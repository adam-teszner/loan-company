const sortOrder = new URLSearchParams(window.location.search).getAll('order_by')


let setAscending = (headerId) => {
    document.getElementById(headerId).className = "table-th active";
    document.getElementById(headerId).querySelector("#sort-icon").innerHTML = "&#8595";
}

let setDescending = (headerId) => {
    document.getElementById(headerId).className = "table-th active";
    document.getElementById(headerId).querySelector("#sort-icon").innerHTML = "&#8593";
}

setStyle = () => {
    let id;
    if (sortOrder.length < 1){
        return;
    }

    for (let param of sortOrder) {
        if (param.startsWith('-')){
            id = param.split('-')[1];
            setAscending(id);
        }
        else {
            setDescending(param);
        }
    }
    id = sortOrder[0].split('-')[1] || sortOrder[0];
    document.getElementById(id).className = "table-th active-primary";
}

setStyle();