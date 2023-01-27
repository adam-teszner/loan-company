let searchInputField = document.querySelectorAll('.search-input');
let queryParams = new URLSearchParams();
const searchBtn = document.querySelector('#search-btn');
const baseUrl = '/search/q?format=datatables';
const checkBox = document.querySelector('#sadb');
const prodTable = $('#products').DataTable({
    responsive: true,
    pageLength: 50,
    lengthChange: false,
    initComplete: function(){
        $('.dataTables_wrapper').addClass('data-table-cont');
        $('.dataTables_filter input').addClass('pyl-input pyl-dt-search');
        $('.dataTables_filter label').addClass('t-fam-raj');
        $('.dataTables_info').addClass('step-links t-size-0-9');
        $('.dataTables_paginate').addClass('step-links t-size-0-9');
    },
    'columnDefs': [
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


searchBtn.addEventListener('click', () => {

    // Applies query string to datatables and 
    // reloads the table on clicking "search" button

    let queryUrl = baseUrl + '&' + queryParams.toString();
    // console.log(queryUrl);
    prodTable.ajax.url(queryUrl);
    prodTable.ajax.reload();

} );

    // switches on/off search all database parameter
checkBox.addEventListener('click', () =>
    checkBox.checked === true ? queryParams.append(checkBox.name, 'on') : queryParams.delete(checkBox.name)    
)