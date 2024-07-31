// script.js

function show_form() {
    document.getElementById("form").style.display = "block";
}

function hide_form() {
    document.getElementById("form").style.display = "none";
}

function show_error(message) {
    document.getElementById("error").innerHTML = message;
    document.getElementById("error").style.display = "block";
    setTimeout(function() {
        document.getElementById("error").style.display = "none";
    }, 2000);
}

function mark_done(item) {
    fetch(`/mark/${encodeURIComponent(item)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to mark as done");
            }
            return response.json();
        })
        .then(() => window.location.reload())
        .catch(error => show_error(error.message));
}

function delete_item(item) {
    fetch(`/delete/${encodeURIComponent(item)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to delete item");
            }
            return response.json();
        })
        .then(() => window.location.reload())
        .catch(error => show_error(error.message));
}

document.querySelectorAll('.mark-as-done').forEach(button => {
    button.addEventListener('click', () => {
        mark_done(button.getAttribute('data-item'));
    });
});

document.querySelectorAll('.delete-item').forEach(button => {
    button.addEventListener('click', () => {
        delete_item(button.getAttribute('data-item'));
    });
});

// function fetchItems() {
//     $.getJSON("/api/items", function(data) {
//         let htmlStr = data.map(function(item) {
//             return `<tr>
//                         <td class="${item.status}">${item.what_to_do}</td>
//                         <td class="${item.status}">${item.due_date}</td>
//                         <td>
//                             <button onclick="markAsDone('${item.what_to_do}')">mark as done</button>
//                             <button onclick="deleteItem('${item.what_to_do}')">delete</button>
//                         </td>
//                     </tr>`;
//         }).join("");
//         $("#todo_table").html(htmlStr);
//     });
// }

// function toggle_entry_form() {
//     $("#add_form").toggle();
//     $("#toggle_button").text(
//         $("#add_form").is(":visible") ? "cancel the new entry" : "add a new item"
//     );
// }

// $("#add_form").submit(function(event) {
//     event.preventDefault();
//     let newItem = {
//         "what_to_do": $("#what_to_do").val(),
//         "due_date": $("#due_date").val(),
//         "status": ""
//     };
//     $.ajax({
//         url: "/api/items",
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify(newItem),
//         success: function(response) {
//             $("#what_to_do").val("");
//             $("#due_date").val("");
//             $("#add_form").hide();
//             $("#toggle_button").text("add a new item");
//             fetchItems();
//         },
//         error: function() {
//             alert("Failed to add item!");
//         }
//     });
// });

// function deleteItem(item) {
//     $.ajax({
//         url: "/api/items/" + encodeURIComponent(item),
//         type: "DELETE",
//         success: fetchItems,
//         error: function() {
//             alert("Failed to delete item!");
//         }
//     });
// }

// function markAsDone(item) {
//     $.ajax({
//         url: "/api/items/" + encodeURIComponent(item),
//         type: "PUT",
//         success: fetchItems,
//         error: function() {
//             alert("Failed to mark item as done!");
//         }
//     });
// }

// $(document).ready(fetchItems);

