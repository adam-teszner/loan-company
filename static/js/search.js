let searchInputField = document.querySelectorAll('.search-input');
let queryParams = new URLSearchParams();
const expandShrink = document.getElementById('search-expand');
const searchBtn = document.querySelector('#search-btn');
const genPDFBtn = document.querySelector('#gen-pdf-btn');
const pdfUrl = '/search/p';
const baseUrl = '/search/q?format=datatables';
const checkBox = document.querySelector('#sadb');

const prodTable = $('#products').DataTable({
    serverSide: true,
    searchDelay: 800,
    responsive: true,
    pageLength: 50,
    lengthChange: false,
    paging: true,
    select: true,
    initComplete: function(){
        $('.dataTables_wrapper').addClass('data-table-cont');
        $('.dataTables_filter input').addClass('pyl-input pyl-dt-search');
        $('.dataTables_filter label').addClass('t-fam-raj');
        $('.dataTables_info').addClass('step-links t-size-0-9');
        $('.dataTables_paginate').addClass('step-links t-size-0-9');
        $('.paginate_button').addClass('pyl-dt-step-hover');
        $('.current').addClass('pyl-dt-current');
    },
    'columnDefs': [
    {targets: 3,
    data: 'owner.social_security_no_pesel',
    row: 'owner.url',    
    render: function(data, type, row) {
        return `<a href="${row.owner.url.split('?')[0]}">${data}</a>`
    }},
    {className: 't-fam-raj t-size-0-9', targets: '_all'},
    {responsivePriority: 10010, targets: 8},
    {responsivePriority: 10009, targets: 7},
    {responsivePriority: 10008, targets: 5},
    {responsivePriority: 10007, targets: 6},
    {responsivePriority: 10006, targets: 4},
    {responsivePriority: 10005, targets: 10},
    ],
  });

searchInputField.forEach(input => {

    // Creates a Query String based on inputs

    input.addEventListener('focusout', (e) => {        
        if (input.value.trim() === '') {
            if (queryParams.has(input.name)) {
                queryParams.delete(input.name);
            }else {
                return null
            }
        }else {
            queryParams.delete(input.name);
            queryParams.append(input.name, input.value);
        }
    });
});

generatePdf = (url) => {
    let requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };
    
    fetch(url, requestOptions)
      .then(response => response.blob())
      .then(data => {
        var a = document.createElement('a');
        a.href = window.URL.createObjectURL(data);
        if (a.type == 'application/x-zip-compressed'){
                a.download = 'FILENAME';
        }
        a.click();
    })
      .catch(error => console.log('error', error));
}


searchBtn.addEventListener('click', () => {

    // Applies query string to datatables and 
    // reloads the table on clicking "search" button
    let currentPage = document.querySelector('paginate_button current');
    let queryUrl = baseUrl + '&' + queryParams.toString();
    prodTable.ajax.url(queryUrl);
    prodTable.ajax.reload();

} );

genPDFBtn.addEventListener('click', () => {

    // Generates query params based on selected rows in the table
    // If none selected every item on page is added to query params
    console.log('CLICK');
    let rowData = prodTable.rows( { selected: true } ).data();
    console.log("RowData", rowData.length);
    if (rowData.length == 0){
        rowData = prodTable.rows( { selected: false } ).data();
    }

    let idList = [];
    let currentPage = document.getElementsByClassName('paginate_button current')[0];
    for (let [k,v] of Object.entries(rowData)){
        if (!isNaN(k)){
            idList.push(rowData[k].id);
        }
    };
    let queryUrl = pdfUrl + '?id=' + idList.join();
    generatePdf(queryUrl);
} );

    // switches on/off search all database parameter
checkBox.addEventListener('click', () =>
    checkBox.checked === true ? queryParams.append(checkBox.name, 'on') : queryParams.delete(checkBox.name)    
)

expandShrink.addEventListener('click', () => {
    let searchBottom = document.querySelector('.search-bottom');
    if (searchBottom.classList.contains('form-hide')) {
        searchBottom.classList.remove('form-hide');
        expandShrink.innerHTML = "Shrink";
    }else {
        searchBottom.classList.add('form-hide');
        expandShrink.innerHTML = "Expand";
    }
});