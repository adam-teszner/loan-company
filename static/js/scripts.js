let nav = document.getElementById('navbar').classList;
let menu = document.getElementById('menu-ic').classList;
let closeMen = document.getElementById('close-ic').classList;


function openMenu() {

    if (nav.contains('menu-invisible') && closeMen.contains('menu-invisible')) {
        var cl = nav.remove('menu-invisible'); closeMen.remove('menu-invisible'); menu.add('menu-invisible');
        return cl
    } else {
        var op =  nav.add('menu-invisible'); closeMen.add('menu-invisible'); menu.remove('menu-invisible');
        return op
       
    }
}





let userInfoTooltip = document.getElementById('user-info');
let userIcon = document.getElementById('account_icon');
var timeout;

function userTooltipShow () {
    if(window.innerWidth > 1050) {
        clearTimeout(timeout);
        userInfoTooltip.style.display = 'block';
        // console.log('one');
    } else {}
}

function userTooltipHide () {
    if(window.innerWidth > 1050) {
        timeout = setTimeout(() => {userInfoTooltip.style.display = 'none';},300);
    } else {}
}

userIcon.addEventListener('mouseover', userTooltipShow);
userIcon.addEventListener('mouseout', userTooltipHide);
userInfoTooltip.addEventListener('mouseover', userTooltipShow);
userInfoTooltip.addEventListener('mouseout', userTooltipHide);


// not sure it its efficient ! 


// TABLE column sorting looks  // 


if (sort_order.length > 0) {
    for (let th = 1; th < sort_order.length; th++) {
        if (sort_order[th].startsWith('-')) {
            var id_desc = sort_order[th].slice(1);
            var add_class = document.getElementById(id_desc).classList.add('active');
            var remove_primary = document.getElementById(id_desc).classList.remove('active-primary');
            var arrow = document.getElementById(id_desc).querySelector('#sort-icon').innerHTML = '&#8593';
            // console.log('jeden');
        }else{
            var id_asc = sort_order[th];
            var add_class = document.getElementById(id_asc).classList.add('active');
            var remove_primary = document.getElementById(id_asc).classList.remove('active-primary');
            var arrow = document.getElementById(id_asc).querySelector('#sort-icon').innerHTML = '&#8595';
            // console.log('dwa');
        }

    }
    if (sort_order[0].startsWith('-')) {
        var id_desc = sort_order[0].slice(1);
        var add_class = document.getElementById(id_desc).classList.add('active-primary');
        var remove_primary = document.getElementById(id_desc).classList.remove('primary');
        var arrow = document.getElementById(id_desc).querySelector('#sort-icon').innerHTML = '&#8593';
        // console.log('ZERO');
    }else{
        var id_asc = sort_order[0];
        var add_class = document.getElementById(id_asc).classList.add('active-primary');
        var remove_primary = document.getElementById(id_asc).classList.remove('primary');
        var arrow = document.getElementById(id_asc).querySelector('#sort-icon').innerHTML = '&#8595';
        // console.log('Nie-zero');
    }


}else {
    // console.log('blank');
}


function formNextPage () {
    var form_step = document.getElementsByClassName('form-step');
    var step_no = document.getElementsByClassName('step');
    var button_prev = document.getElementById('btn-prev');
    var button_next = document.getElementById('btn-next');
    var button_finish = document.getElementById('btn-finish');


    for (var z = 0; z < form_step.length; z++) {
        if (form_step[z].classList.contains('form-hide') === false && z !== form_step.length-2) {
            
            return form_step[z].classList.add('form-hide'), 
                    form_step[z+1].classList.remove('form-hide'),
                    step_no[z+1].classList.add('step-color'),
                    button_prev.classList.remove('btn-hide')
        }else if (form_step[z].classList.contains('form-hide') === false) {
            
            return form_step[z].classList.add('form-hide'),
                    form_step[z+1].classList.remove('form-hide'),
                    step_no[z+1].classList.add('step-color'),
                    button_next.classList.add('btn-hide'),
                    button_finish.classList.remove('btn-hide')
        }else {}
    }

}

function formPreviousPage () {
    var form_step = document.getElementsByClassName('form-step');
    var step_no = document.getElementsByClassName('step');
    var button_prev = document.getElementById('btn-prev');
    var button_next = document.getElementById('btn-next');
    var button_finish = document.getElementById('btn-finish');

    for (var z = 1; z < form_step.length; z++) {
        if (form_step[z].classList.contains('form-hide') === false && z == form_step.length-1){
            button_prev.classList.remove('btn-hide'),
            button_finish.classList.add('btn-hide'),
            button_next.classList.remove('btn-hide'),
            form_step[z].classList.add('form-hide'),
            form_step[z-1].classList.remove('form-hide'),
            step_no[z].classList.remove('step-color')
        }
            
        else if (form_step[z].classList.contains('form-hide') === false && z !== 0 ){
            button_prev.classList.remove('btn-hide'),
            form_step[z].classList.add('form-hide'),
            form_step[z-1].classList.remove('form-hide'),
            step_no[z].classList.remove('step-color')
        }else{
            button_prev.classList.add('btn-hide')
        }
    }
}

// MOZNA TO BYLO ZROBIC PRZY POMOCY SPRAWDZENIA NA KTOREJ JESTEM STRONIE...