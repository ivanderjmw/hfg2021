$(document).ready(function () {
  initDragDrop();
});

function initDragDropSets(institutions) {
  return new Array(institutions.length).fill(0).map(()=> new Set());
}

function initDragDrop() {
  const icolumns = 4;
  const stakeholders = ["Students", "Workers", "Police"];
  const institutions = ["University", "Factory", "Police Headquarters"];

  const dragDropSets = initDragDropSets(institutions);
  let removeIntent = false;

  $("ul, li").disableSelection();

  stakeholders.map((stakeholder, index) => {
    var draggableElement = $("<ul></ul>").text(stakeholder);
    draggableElement.addClass("draggable");
    draggableElement.addClass("list-group-item");
    draggableElement.attr("id", `stakeholders-${index}`);
    draggableElement.attr("data", index);

    draggableElement.draggable({
      connectToSortable: ".sortable",
      helper: "clone",
      opacity: 0.5,
      revert: "invalid",
      start: () => {
        $(".institution-notif").text("Drop unique stakeholders here");
      },
      stop: () => {
        $(".institution-notif").text("");
      }
    });
    $(".stakeholders-list-group").append(draggableElement);
    
  });

  var institutionsContainer = $(".institutions-container");
  var rowNum = 0;
  institutions.map((institution, index) => {
    if (index % icolumns === 0) {
      rowNum++;
      const rowElement = $("<div class='row'></div>");
      rowElement.attr("id", `row-${rowNum}`);
      institutionsContainer.append(rowElement);
    }
    const colElement = $("<div class='col'></div>");
    colElement.addClass("institution-body");
    colElement.addClass(["border", "border-dark", "rounded", "m-2", "p-2"]);

    const nameElement = $("<h3></h3>").text(institution);
    const sortableElement = $("<ul></ul>");
    sortableElement.attr("id", `institutions-${index}`);
    sortableElement.attr("data", index);
    sortableElement.addClass("list-group");
    sortableElement.addClass("sortable");

    sortableElement.sortable({
      revert: true,
      placeholder: "placeholder"
      
    });

    sortableElement.on("sortreceive", function(event, ui) {
      
      var pasteItem = !dragDropSets[$(this).attr("data")].has(ui.item.attr("data"));

      if (pasteItem) {
        dragDropSets[index].add(ui.item.attr("data"));
      } else {
        $(this).data().uiSortable.currentItem.remove()
      }
      // AJAX REQUEST HERE
      console.log($(this).children());
      console.log(dragDropSets[index]);

    });

    const notifierElement = $("<small></small>");
    notifierElement.addClass("institution-notif");


    colElement.append(nameElement, sortableElement, notifierElement);
    $(`#row-${rowNum}`).append(colElement);
  });

  $(".trash").droppable({
    accept: ".sortable, .draggable",
    activate: function(event, ui) {
      $(this).css("background-color", "#efefef");
      $(this).addClass(["border", "border-radius", "border-secondary"]);
      $(this).text("Drop here to remove");
      
    },
    deactivate: function(event, ui) {
      $(this).css("background-color", "transparent");
      $(this).removeClass(["border", "border-radius", "border-secondary"]);
      $(this).text("");
    },
    drop: function(event, ui) {
      ui.helper.remove();
      $(this).css("background-color", "transparent");
      $(this).removeClass(["border", "border-radius", "border-secondary"]);
    },

  });
  
}