function searchTransaction() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById('btn-search');
  filter = input.value.toUpperCase();
  table = document.querySelector("table tbody");
  rowsTable = table.getElementsByTagName("tr");

  for (i = 0; i < rowsTable.length; i++) {
    titleColumn = rowsTable[i].getElementsByTagName("td")[0];
    if (titleColumn) {
      txtValue = titleColumn.textContent || titleColumn.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        rowsTable[i].style.display = "";
      } else {
        rowsTable[i].style.display = "none";
      }
    }
  }
}
