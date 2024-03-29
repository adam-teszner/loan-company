const nav = document.getElementById('navbar').classList;
const menu = document.getElementById('menu-ic').classList;
const closeMen = document.getElementById('close-ic').classList;

function openMenu() {
    if (nav.contains('menu-invisible') && closeMen.contains('menu-invisible')) {
        var cl = nav.remove('menu-invisible'); closeMen.remove('menu-invisible'); menu.add('menu-invisible');
        return cl
    } else {
        var op =  nav.add('menu-invisible'); closeMen.add('menu-invisible'); menu.remove('menu-invisible');
        return op
       
    }
}


const userInfoTooltip = document.getElementById('user-info');
const userIcon = document.getElementById('account_icon');
var timeout;

function userTooltipShow () {
    if(window.innerWidth > 949) {
        clearTimeout(timeout);
        userInfoTooltip.style.display = 'block';
        // console.log('one');
    } else {}
}

function userTooltipHide () {
    if(window.innerWidth > 949) {
        timeout = setTimeout(() => {userInfoTooltip.style.display = 'none';},300);
    } else {}
}

userIcon.addEventListener('mouseover', userTooltipShow);
userIcon.addEventListener('mouseout', userTooltipHide);
userInfoTooltip.addEventListener('mouseover', userTooltipShow);
userInfoTooltip.addEventListener('mouseout', userTooltipHide);


function formNextPage () {
    var form_step = document.getElementsByClassName('form-step');
    var step_no = document.getElementsByClassName('step');
    var button_prev = document.getElementById('btn-prev');
    var button_next = document.getElementById('btn-next');
    var button_finish = document.getElementById('btn-finish');
    var step_line = document.getElementsByClassName('step-line');


    for (var z = 0; z < form_step.length; z++) {
        if (form_step[z].classList.contains('form-hide') === false && z !== form_step.length-2) {
            
            return form_step[z].classList.add('form-hide'), 
                    form_step[z+1].classList.remove('form-hide'),
                    step_no[z+1].classList.add('step-color'),
                    button_prev.classList.remove('btn-hide'),
                    step_line[z].classList.add('line-color')
        }else if (form_step[z].classList.contains('form-hide') === false) {
            
            return form_step[z].classList.add('form-hide'),
                    form_step[z+1].classList.remove('form-hide'),
                    step_no[z+1].classList.add('step-color'),
                    button_next.classList.add('btn-hide'),
                    button_finish.classList.remove('btn-hide'),
                    step_line[z].classList.add('line-color')
        }else {}
    }

}

function formPreviousPage () {
    var form_step = document.getElementsByClassName('form-step');
    var step_no = document.getElementsByClassName('step');
    var button_prev = document.getElementById('btn-prev');
    var button_next = document.getElementById('btn-next');
    var button_finish = document.getElementById('btn-finish');
    var step_line = document.getElementsByClassName('step-line');

    for (var z = 1; z < form_step.length; z++) {
        if (form_step[z].classList.contains('form-hide') === false && z == form_step.length-1){
            button_prev.classList.remove('btn-hide'),
            button_finish.classList.add('btn-hide'),
            button_next.classList.remove('btn-hide'),
            form_step[z].classList.add('form-hide'),
            form_step[z-1].classList.remove('form-hide'),
            step_no[z].classList.remove('step-color'),
            step_line[z-1].classList.remove('line-color')
        }
            
        else if (form_step[z].classList.contains('form-hide') === false && z !== 0 ){
            button_prev.classList.remove('btn-hide'),
            form_step[z].classList.add('form-hide'),
            form_step[z-1].classList.remove('form-hide'),
            step_no[z].classList.remove('step-color'),
            step_line[z-1].classList.remove('line-color')
        }else{
            button_prev.classList.add('btn-hide')
        }
    }
}

// MOZNA TO BYLO ZROBIC PRZY POMOCY SPRAWDZENIA NA KTOREJ JESTEM STRONIE...



var json_data;

function checkPesel () {
    var peselCheck = new XMLHttpRequest();
    var peselInput = document.getElementById('id_social_security_no_pesel').value;

    // PESEL quick validation

    if (peselInput.length === 11) {
        peselInput = document.getElementById('id_social_security_no_pesel').value;
        peselCheck.open('GET', 'custom_create?pesel='+peselInput);
        peselCheck.send()
    } else {}

    peselCheck.onreadystatechange = function success () {
        var DONE = 4;
        var OK = 200;
        

        if (peselCheck.readyState === DONE) {
            if (peselCheck.status === OK && peselCheck.responseText !== 'Error') {
                // console.log(peselCheck.responseText);
                json_data = JSON.parse(peselCheck.responseText);
                document.getElementById('customer_id_value').setAttribute('value', json_data[0]['pk']);
                let showModal = document.getElementById('pyl-modal');
                let modalBtn = document.getElementById('pyl-modal-ok');
                let creator = json_data[4].creator_first_name + ' ' + json_data[4].creator_last_name;

                showModal.style.display = 'block';
                document.getElementById('modal-first_name').innerHTML = json_data[0].fields.first_name;
                document.getElementById('modal-last_name').innerHTML = json_data[0].fields.last_name;
                document.getElementById('modal-pesel').innerHTML = json_data[0].fields.social_security_no_pesel;
                document.getElementById('modal-created_by').innerHTML = creator;


                modalBtn.onclick = function () {
                    showModal.style.display = 'none';
                    // filling customer object
                    for (let [key, value] of Object.entries(json_data[0]['fields'])) {
                        let chng_value = document.getElementById('id_'+key);
                        if (chng_value !== null && chng_value.children.length === 0) {
                            chng_value.value = value;
                            // console.log(value);
                        }else if (chng_value !== null && chng_value.children.length > 0) {
                            for (let child_no = 0; child_no < chng_value.children.length; child_no++) {
                                if (chng_value.children[child_no].value === value) {
                                    for (let c of chng_value.children) {
                                        // CHANGING THIS FOR SAFARI COMPATIBILITY !!!
                                        // c.removeAttribute('selected')
                                        c.selected = false;
                                    }
                                    chng_value.children[child_no].selected = true;
                                }else{} 
                            }
                        }else{}
                    }
                    // filling customer adress
                    for (let [key, value] of Object.entries(json_data[1]['fields'])) {
                        let chng_value = document.getElementById('id_customer_adress-'+key);
                        if (chng_value !== null) {
                            chng_value.value = value;
                            // console.log(chng_value);
                        }else{
                            console.log('PUSTE');
                        }
                    }

                    // filling workplace
                    for (let [key, value] of Object.entries(json_data[2]['fields'])) {
                        let chng_value = document.getElementById('workplace_id_workplace_form-'+key);
                        if (chng_value !== null && chng_value.children.length === 0) {
                            chng_value.value = value;
                            // console.log(value);
                        }else if (chng_value !== null && chng_value.children.length > 0) {
                            for (let child_no = 0; child_no < chng_value.children.length; child_no++) {
                                if (chng_value.children[child_no].value === value) {
                                    for (let c of chng_value.children) {
                                        // CHANGING THIS FOR SAFARI COMPATIBILITY !!!
                                        // c.removeAttribute('selected')
                                        c.selected = false;
                                    }
                                    chng_value.children[child_no].selected = true;
                                }else{} 
                            }
                        }else{}
                    }
                    // filling workplace adress
                    for (let [key, value] of Object.entries(json_data[3]['fields'])) {
                        let chng_value = document.getElementById('id_workplace_adr_form-'+key);
                        if (chng_value !== null) {
                            chng_value.value = value;
                            // console.log(chng_value);
                        }else{
                            console.log('PUSTE');
                        }
                    }
                }

            }else{
                console.log('error' + peselCheck.status);
                console.log(peselCheck.responseText);
            }
        }
    
    }
    
    

}

// in SAFARI - removeAttribute/setAttribute (in case of SELECTED option in form) doesnt update the website..
// Use .selected true/false instead


function resetForm() {
    let inputs = document.getElementsByTagName('input');
    let selects = document.getElementsByTagName('select');

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].name !== 'csrfmiddlewaretoken') {
            inputs[i].value = '';
        }else{}
    }

    for (let s = 0; s < selects.length; s++) {
        for (let c = 0; c < selects[s].childElementCount; c++){
            selects[s].children[c].selected = false;
        }
        selects[s].children[0].selected = false;

    }
}

// animation for expanding/collapsing tables

function expandTable (id) {

    // console.log(id);
    
    document.getElementById('expanded-'+id).classList.add('pyl-hidden');
    document.getElementById('collapsed-'+id).classList.remove('pyl-hidden');
    
    let tableAnimation = document.getElementById('table-'+id);
    tableAnimation.classList.remove('pyl-hidden');
    tableAnimation.classList.add('pyl-unfold');

    tableAnimation.addEventListener('animationend', () => {
        tableAnimation.classList.remove('pyl-unfold');
    }, {once: true}) //KLUCZ !! bo cały czas działał event listener ! 

}

function shrinkTable (id) {

    document.getElementById('collapsed-'+id).classList.add('pyl-hidden');
    document.getElementById('expanded-'+id).classList.remove('pyl-hidden');
    
    let tableAnimation = document.getElementById('table-'+id);
    tableAnimation.classList.add('pyl-fold');

    
    tableAnimation.addEventListener('animationend', () => {
        tableAnimation.classList.add('pyl-hidden');
        tableAnimation.classList.remove('pyl-fold');
        
    }, {once: true})

    
}

const showUserMenu = document.getElementById('account_icon');
const mobileAccTooltip = document.querySelectorAll('.mob-acc-tooltip')[0];
const accIcon = document.querySelectorAll('.account-icon-2')[0].innerHTML;
const currentUser = document.querySelectorAll('.user-names')[0].innerHTML;

showUserMenu.addEventListener('click', () => {
    if (window.innerWidth < 950 ){
        if (mobileAccTooltip.classList.contains('menu-invisible') === true ) {
            showUserMenu.innerHTML = `${currentUser}`;
            showUserMenu.classList.add('acc-wide');
        } else {
            showUserMenu.innerHTML = `${accIcon}`;
            showUserMenu.classList.remove('acc-wide');
        }
        mobileAccTooltip.classList.toggle('menu-invisible');
    }
})

window.addEventListener('resize', () => {
    if (window.innerWidth > 950  &&  !nav.contains('menu-invisible') && !closeMen.contains('menu-invisible')) {
        mobileAccTooltip.classList.add('menu-invisible');
        nav.add('menu-invisible');
        closeMen.add('menu-invisible');
        menu.remove('menu-invisible');
    }
    showUserMenu.innerHTML = accIcon;
    showUserMenu.classList.remove('acc-wide');
})