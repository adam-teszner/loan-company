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