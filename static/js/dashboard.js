// Change color of Gold Balance row
if (document.getElementById("col-Gold-Balance").innerHTML < 0) {
    document.getElementById("row-Gold-Balance").setAttribute("class", "table-danger");
}
else if (document.getElementById("col-Gold-Balance").innerHTML > 0) {
    document.getElementById("row-Gold-Balance").setAttribute("class", "table-success");
};

// Change color of Gold Balance row
if (document.getElementById("col-Cash-Balance").innerHTML < 0) {
    document.getElementById("row-Cash-Balance").setAttribute("class", "table-danger");
}
else if (document.getElementById("col-Cash-Balance").innerHTML > 0) {
    document.getElementById("row-Cash-Balance").setAttribute("class", "table-success");
};

function warnUserDel(itmID){
    warnUsr = confirm("Do you really want to Delete this Item?")
    DelElement = document.getElementById(itmID)
    if (warnUsr==true) {
        window.location.replace(itmID);
    } else {
        alert("Don't Worry It's not Deleted!!");
    };
};

// Set up Modal for names in table
const nameModal = document.getElementById('nameModal');
nameModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    const button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    let id = button.getAttribute('data-bs-id')
    let tabNo = button.getAttribute('data-bs-tab-no');
    let name = button.getAttribute('data-bs-name');
    let category = button.getAttribute('data-bs-category');
    let amt = button.getAttribute('data-bs-amt');
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    let modalTitle = nameModal.querySelector('#nameModalLabel');
    let amtLabel = nameModal.querySelector('#item-amt-label');
    let itemId = nameModal.querySelector('#item-id');
    let itemName = nameModal.querySelector('#item-name');
    let itemCat = nameModal.querySelector('#item-cat');
    let itemAmt = nameModal.querySelector('#item-amt');

    let filterName = nameModal.querySelector('#filterName');
    let updateItem = nameModal.querySelector('#updateItem');
    let delBtn = nameModal.querySelector('.modal-del-btn');

    modalTitle.innerHTML = `View Data From: ${name}`;
    if (category == 'Gold'){
        amtLabel.innerHTML = 'Weight';
    } else {
        amtLabel.innerHTML = 'Price';
    };

    itemId.innerHTML = tabNo;
    itemName.innerHTML = name;
    itemCat.innerHTML = category;
    itemAmt.innerHTML = amt;

    // Make buttons Functional
    // Filter Button
    filterName.innerHTML = `Filter By: "${name}"`;
    filterName.setAttribute('href', `/Filter/Name/${name}`)

    // Update Button
    updateItem.setAttribute('href', `/${category}/update/${id}`);

    // Delete Button
    delBtn.setAttribute('id', `/${category}/delete/${id}`)
})