const modal = document.getElementsByClassName('pyl-modal-background')[0];
const form = document.getElementById('edit-form');
const inputs = document.getElementById('form-inputs');
const pencilIcon = document.getElementsByClassName('edit-ic');
let dataObj;

let res;

editModal = (url, headerText) => {
    let dataObj;
    let requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };
    
    fetch(url, requestOptions)
      .then(response => response.json())
      .then(data => {
        dataObj = data
        drawForms(dataObj.schema)
            .then(initialFill(dataObj.initial));
        document.getElementById('pyl-modal-save').setAttribute('url', url);
        listenForId();
        document.getElementById('modal-header').innerHTML = 
        `Edit ${headerText.charAt(0).toUpperCase()+headerText.slice(1)}`;
        modal.style.display = 'block';
      })
      .catch(error => console.log('error', error));
}

closeEdit = () => {
    document.getElementsByClassName('pyl-modal-background')[0].removeAttribute('style');
    inputs.innerHTML = '';
}


drawForms = (jsonData, parentId) => {
    parentId = (parentId === undefined) ? '' : `${parentId}__`;

    // objects below are because of schema format django sends...
    const inputTypes = {
        string: 'text',
        integer: 'number',
    }
    // taken directly from django rest framework attrs 
    const simpleVal = {
        // read_only: 'readonly',
        min_length: 'minlength',
        max_length: 'maxlength',
        min_value: 'min',
        max_value: 'max',
    }

    let form = document.getElementById('edit-form');
    for (let [k,v] of Object.entries(jsonData)){
        let id = `${parentId}${k}`;
        let inputType = (inputTypes[v.type] !== undefined) ? inputTypes[v.type] : v.type;
        let req = (v.required) ? 'required' : '';

        if (v.type === 'nested object') {
            drawForms(v.children, id)
            continue;
        }
        if (v.type === 'choice') {
            
            inputs.innerHTML += `<div class="pyl-edit-inputs">
                                <label class="pyl-label-text" for=${id+'-id'}>${v.label}</label>
                                <img class="edit-ic" src=${editIcon}>
                                <select disabled class="pyl-input" id=${id+'-id'} name=${k} ${req}><option value selected></option>
                                <div class="error-msg" id=${id+'-msg'}</div>`
            let selTag = document.getElementById(`${id+'-id'}`)
            for (let i of v.choices) {
                selTag.innerHTML += `<option value=${i.value}>${i.display_name}</option>`
            }
            inputs.innerHTML += '</select></div>'
            
        }else {
            // To trzeba zmienic - za duzo for loopow ! 
            let attributes = ''
            for (let [a,b] of Object.entries(v)){
                let attr = (simpleVal[a] !== undefined) ? `${simpleVal[a]}=${b}` : '';
                attributes += attr+' ';
            }
            inputs.innerHTML += `<div class="pyl-edit-inputs">
                                <label class="pyl-label-text" for=${id+'-id'}>${v.label}</label>
                                <img class="edit-ic" src=${editIcon}>
                                <input disabled class="pyl-input" type=${inputType} name=${k} id=${id+'-id'} ${req} ${attributes}>
                                <div class="error-msg" id=${id+'-msg'}></div></div>`;
        }
    }
    modal.style.display = 'block'
    return new Promise((resolve, reject) => {
        const error = false
        if (!error) {
            resolve();
        }else {
            reject('Errror !');
        }
    })
}

initialFill = (initial, parentId) => {
    parentId = (parentId === undefined) ? '' : `${parentId}__`;
    let id;
    let formInput;
    // console.log(parentId)
    for (let [k,v] of Object.entries(initial)) {
        id =`${parentId}${k}`;
        if (typeof v == 'object') {
            // console.log(v)
            initialFill(v, id);
            continue;
        }
        formInput = document.getElementById(`${id+'-id'}`);
        formInput.value = v;
    }
}


formToJson = (inputsDivId) => {
    // inputsDivID is <DIV id=""> where all the children are <INPUTs>, usually it is <FORM> instead of <DIV>
    // but it all depends on website layout
    
    let form = document.getElementById(`${inputsDivId}`);
    let formKeys;
    let value;
    let value2;


    let formObj = {}
    let fomrObjHuman = {}
    for (let child of form.querySelectorAll('input, select, textarea')) {

        if (child.disabled) {
            continue;
        }

        formKeys = child.id.slice(0, -3).split('__');
        value = child.value
        if (child.type === 'select-one') {
            value2 = child.options[child.selectedIndex].text;
        }else if (child.type === 'date') {
            value2 = child.valueAsDate.toDateString().slice(4);
        }else {
            value2 = child.value
        }
        
        assign(formObj, fomrObjHuman, formKeys, value, value2)

    }
    // console.log(formObj)
    // console.log(JSON.stringify(formObj))
    return [formObj, fomrObjHuman]

}

assign = (obj, obj2, keyPath, value, value2) => {
    const lastKeyIndex = keyPath.length-1;
        for (let i = 0; i < lastKeyIndex; i++) {
            const key = keyPath[i];
            if (!(key in obj)){
            obj[key] = {}
            obj2[key] = {}
            }
        obj = obj[key];
        obj2 = obj2[key];
    }
    obj[keyPath[lastKeyIndex]] = value;
    obj2[keyPath[lastKeyIndex]] = value2;
}

saveFormData = (inputsDivId, url) => {
    // (() => document.querySelectorAll('.error-msg').forEach(element => element.innerHTML = ''))();
    removeValidationErorrs();
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];
    // console.log(cookieValue)
    let headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", cookieValue);
    let formResultArray = formToJson(inputsDivId);
    let rawData = formResultArray[0];
    let humanData = formResultArray[1];
    let formData = JSON.stringify(rawData);
    console.log(formData)
    
    let requestOptions = {
        method: 'PATCH',
        headers: headers,
        body: formData,
        redirect: 'follow'
      };

    let responseStatus;
    fetch(url, requestOptions)
      .then(response => {
        responseStatus = response.status;
        let result = response.json()
        res = result
        // console.log(res, 'PIERWSZA WERSJA')
        return result
      })
      .then(result => {
        switch (responseStatus) {
            case 200:
                // console.log(result);
                closeEdit();
                updateOldData(humanData);
                break
            case 400:
                // console.log(result, 'DRUGA WERSJA');
                // console.log(typeof result)
                // res = result
                validationError(result);
                break
            case 500:
                console.log('500 ERROR - unique nested validator')
                break
        }
      })
      .catch(error => console.log('error', error.toString()));
}

//// not very efficient solution because its copied from above... 
//// should have made one function like getID () => 
//// and then call it now and then... do zmiany w przyszlosci !
updateOldData = (humanData, parentId) => {
    parentId = (parentId === undefined) ? '' : `${parentId}__`;
    // console.log(humanData)
    let id;
    let formInput;
    // console.log(parentId)
    for (let [k,v] of Object.entries(humanData)) {
        id =`${parentId}${k}`;
        // console.log(id)
        if (typeof v == 'object') {
            updateOldData(v, id);
            continue;
        }else{
        formInput = document.getElementById(`${id}`);
        formInput.innerHTML = v;
        }
        if (id === 'first_name' || id === 'last_name') {
            document.getElementById(`${id+'-h1'}`).innerHTML = v+' ';
        }
    }

}

validationError = (result, parentId) => {
    parentId = (parentId === undefined) ? '' : `${parentId}__`;
    let id;
    let message;
    let inpt;
    for (let [k,v] of Object.entries(result)) {
        id =`${parentId}${k}`;
        // console.log(id, 'ID')
        // console.log(typeof v, 'value!!')
        if (typeof v == 'object' && !Array.isArray(v)) {            
            validationError(v, id);
            continue;
        }        
        message = document.getElementById(`${id+'-msg'}`);
        message.innerHTML += `${v}`
        inpt = document.getElementById(`${id+'-id'}`);
        inpt.classList.add('val-err');
        // message.setAttribute('error-msg', v);
    }
}

removeValidationErorrs = () => {
    document.querySelectorAll('.error-msg').forEach(element => element.innerHTML = '');
    document.querySelectorAll('.pyl-input').forEach(element => element.classList.remove('val-err'));

}


// listenForId = () => {
//     inputs.addEventListener('click', (e) => {
//         console.log(e.target.id);
//         document.getElementById(e.target.id).disabled = false;
//     })
// }

listenForId = () => {
    for (let icon of pencilIcon) {
        icon.addEventListener('click', (e) => {
            icon.nextElementSibling.toggleAttribute('disabled');
            // console.log(icon.nextElementSibling.id);
        });
    };
};

// na jutro - NAJPIERW ZMIENhIC ID Z LABELI na ID z Key - DONE
// pomyslec nad generowaniem unikatowych id dla kazdych pol - tak zeby mozna bylo - DONE
// wypełnic formy initial data - DONE
// wygenerować Json ze zmienionych form:
    // mozna id> pyl-modal-right.children > iterować:
    // i potem let x child.id = np. adress__street-id
    // x.slice(0, -3) (zostanie adress__street)
    // x.split('__') (zostanie [adress] [street])
    // no i z tego mozna tworzyc jsona
// fetch Patch - DONE

// na koncu - aktualizacja danych !!! - DONE


// problem z validacja unique w workplace nip i phone no .... i tylko tam !! 
// albo rozwiazanie w backend - wskazane ! - DONE (rozwiazanie dorazne- patrz serializers)
// ewentualnie na front-end (pomysl: 
    // zrobić do kazdego inputa dodatkowy atrybut - np. data
    // i w funkcji formToJson zbadać czy 'child'.data === value
    // jesli jest to 'continue' iteracje - czyli pomijamy)

    // moze w przyszlosci...

// dodatkowo - zrobić wszystkie pola DISABLED - i DISABLED nie updatetowac bo po co ? 
// po kliknięciu - pole zrobi się enabled - i tylko enabled będą brane pod uwagę
// przy generowaniu jsona

// DONE

// napisać validation errors massages ! gdzieś muszą się pokazywać ! najlepiej na podstawie
// odpowiedzi error - wskazać trzeba ID znowu ...
// DONE