/**
 * Created by Dhruval Darji on 2/10/16.
 */

/** Setup List **/

var hidden = [];

counter = 0;

function initUL() {

    // Get List from DOM
    document.getElementById('list').innerHTML = "";
    // Create the list element:
    var ul = document.createElement('ul');
    ul.setAttribute('id', 'ul');

    // Finally, return the constructed list:
    document.getElementById('list').appendChild(ul);
}

var addToList = function(item){
    // Get our list
    var ul = document.getElementById('ul');

     // Create the list item:
    var li = newListItem(item);

    // Add it to the list:
    ul.appendChild(li);

    // Update our counter
    counter++;
};

var newListItem = function(item){
    var li = document.createElement('li');
    li.className = "list-item";

    var item_input = newItemInput(item.text);
    var item_size = newItemSize(item.size);
    var item_delete = newItemDelete();

    // Set its contents:
    li.appendChild(item_input);
    li.appendChild(item_size);
    li.appendChild(item_delete);

    return li;
};

var newItemInput = function(text){
    var item = document.createElement('input');
    item.setAttribute("type", "text");
    item.setAttribute("placeholder", "Enter String Here");
    item.className = "input";
    item.value = text;

    item.oninput = function(){
        var nextSibling = item.nextElementSibling;
        nextSibling.innerHTML = "Length: <strong>"+ item.value.length + "</strong>";
    };

    return item;
};

var newItemSize = function(size){
   var item = document.createElement('span');
    item.setAttribute("type", "text");
    item.className = "input-size";
    item.innerHTML = "Length: <strong>"+ size + "</strong>";
    return item;
};

var newItemDelete = function(){
    var span = document.createElement('span');
    span.className = "input-delete";
    var item = document.createElement('button');
    item.setAttribute("type", "text");
    item.className = "btn btn-red";
    item.textContent =  "Delete";

    item.onclick = function() {
        deleteItem(item.parentNode.parentNode);
    };

    span.appendChild(item);
    return span;
};

/** Manipulate List **/

var addItem = function(){
    if(hidden.length > 0){
        addToList(hidden.shift());
    }
    else {
        addToList({
            text: "",
            size: 0
        });
    }
};

var deleteItem = function(li){

    var liText = li.getElementsByClassName("input")[0].value;

    if(counter > 1){
        if(liText !== ""){
            hidden.push(
                {
                    text: liText,
                    size: liText.length
                }
            );
        }

        li.remove();
        counter --;
    }
    else {
        console.log("There must always be atleast one item in the list.")
    }

};

var sortList = function(){
    // Get our List
    var ul = document.getElementById('ul');
    var ul_list = ul.getElementsByTagName('li');

    var list = [];

    var index; //init our index here to avoid duplicate declaration jshint

    // Get and store our list Item Values
    for (index = 0; index < ul_list.length; index++){
        list.push(ul_list[index].getElementsByClassName("input")[0].value);
    }

    // Sort our list values
    list.sort();

    // Re-init our list with sorted values.
    initUL();

    for(index = 0; index < list.length; index++){
        addToList(
            {
                text: list[index],
                size: list[index].length
            }
        );
    }

};

/** Initialize our List **/
initUL();

/** Populate our list with one item. **/
addToList({
    text: "",
    size: 0
});
