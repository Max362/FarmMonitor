//Backend fanction to delete the addeed notes
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    //This will refresh the page
    window.location.href = "/";
  });
}
