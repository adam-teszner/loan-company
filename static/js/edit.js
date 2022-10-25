const modal = document.getElementsByClassName('pyl-modal-background')[0];
const form = document.getElementById('edit-form');
const left = document.getElementsByClassName('pyl-modal-left')[0];
const right = document.getElementsByClassName('pyl-modal-right')[0];
let dataObj;

editModal = (url) => {
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
        modal.style.display = 'block'
      })
      .catch(error => console.log('error', error));
}

closeEdit = () => {
    document.getElementsByClassName('pyl-modal-background')[0].removeAttribute('style');
    left.innerHTML = '';
    right.innerHTML = '';
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
            
            left.innerHTML += `<label for=${id+'-id'}>${v.label}</label>`
            right.innerHTML += `<select id=${id+'-id'} name=${k} ${req}><option value selected></option>`
            let selTag = document.getElementById(`${id+'-id'}`)
            for (let i of v.choices) {
                selTag.innerHTML += `<option value=${i.value}>${i.display_name}</option>`
            }
            right.innerHTML += '</select>'
            
        }else {
            // To trzeba zmienic - za duzo for loopow ! 
            let attributes = ''
            for (let [a,b] of Object.entries(v)){
                let attr = (simpleVal[a] !== undefined) ? `${simpleVal[a]}=${b}` : '';
                attributes += attr+' ';
            }
            
            left.innerHTML += `<label for=${id+'-id'}>${v.label}</label>`;
            right.innerHTML += `<input type=${inputType} name=${k} id=${id+'-id'} ${req} ${attributes}>`;
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
        }else{
        formInput = document.getElementById(`${id+'-id'}`);
        formInput.value = v;
        }
    }
}


formToJson = (inputsDivId) => {
    // inputsDivID is <DIV id=""> where all the children are <INPUTs>, usually it is <FORM> instead of <DIV>
    // but it all depends on website layout
    
    let form = document.getElementById(`${inputsDivId}`);
    let formKeys;
    let value;


    let formObj = {}
    for (let child of form.children) {

        formKeys = child.id.slice(0, -3).split('__');
        // finalKey = formKeys.pop();
        value = child.value
        // console.log(formKeys)
        assign(formObj, formKeys, value)

    }
    console.log(formObj)
    console.log(JSON.stringify(formObj))

}

function assign(obj, keyPath, value) {
    const lastKeyIndex = keyPath.length-1;
        for (let i = 0; i < lastKeyIndex; i++) {
            const key = keyPath[i];
            if (!(key in obj)){
            obj[key] = {}
            }
        obj = obj[key];
    }
    obj[keyPath[lastKeyIndex]] = value;
}




// na jutro - NAJPIERW ZMIENIC ID Z LABELI na ID z Key - DONE
// pomyslec nad generowaniem unikatowych id dla kazdych pol - tak zeby mozna bylo - DONE
// wypełnic formy initial data - DONE
// wygenerować Json ze zmienionych form:
    // mozna id> pyl-modal-right.children > iterować:
    // i potem let x child.id = np. adress__street-id
    // x.slice(0, -3) (zostanie adress__street)
    // x.split('__') (zostanie [adress] [street])
    // no i z tego mozna tworzyc jsona
// fetch Patch
// EWENTUALNIE ! SUBMIT w form-data !!! ????

// na koncu - aktualizacja danych !!!