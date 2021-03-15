$(function () {
  initDragDrop();
});

function initDragDrop() {
  const dragDropSets = new Array(new Set(), new Set(), new Set());
  let removeIntent = false;

  $("ul, li").disableSelection();

  for(let i=0; i<3; i++) {
    $(`#draggable-${i}`).draggable({
      connectToSortable: ".sortable",
      helper: "clone",
      revert: "invalid"
    });
  }

  for(let i=0; i<3; i++) {
    $(`#sortable-${i}`).sortable({
      revert: true,
      over: function() {
        removeIntent = false;
      },
      out: function() {
        removeIntent = true;
      }
    });
  
    $(`#sortable-${i}`).on("sortreceive", function(event, ui) {
      
      var pasteItem = !dragDropSets[i].has(ui.item);
  
      if (pasteItem) {
        dragDropSets[i].add(ui.item);
      } else {
        $(this).data().uiSortable.currentItem.remove()
      }
      console.log(dragDropSets[i]);
    });

    $(`#sortable-${i}`).on("sortbeforestop", function(event, ui) {
      
      if(removeIntent) {
        ui.item.remove();
      }
    });


  }
  
}