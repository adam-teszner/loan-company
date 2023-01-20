let searchInputField = document.querySelectorAll('.search-input');
let queryParams = new URLSearchParams();
const searchBtn = document.querySelector('#search-btn');
const baseUrl = '/search/q?format=datatables';

const prodTable = $('#products').DataTable();

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
    console.log(queryUrl);
    prodTable.ajax.url(queryUrl);
    prodTable.ajax.reload();

} );