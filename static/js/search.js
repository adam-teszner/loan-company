let searchInputField = document.querySelectorAll('.search-input');
let queryParams = new URLSearchParams();
const searchBtn = document.querySelector('#search-btn');
const baseUrl = '/search/q?format=datatables';
const checkBox = document.querySelector('#sadb');
const prodTable = $('#products').DataTable({
    'columnDefs': [
    {className: 't-fam-raj t-size-0-9 cell-width', targets: '_all'},
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