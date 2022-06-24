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


