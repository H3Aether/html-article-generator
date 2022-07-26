const container = document.querySelector(".container");
const footer = document.querySelector(".footer");

function getJsonFile(){
    var file_to_read = document.getElementById("jsonfileinput").files[0];
    var fileread = new FileReader();
    fileread.onload = function(e) {
      var content = e.target.result;
      var intern = JSON.parse(content); // parse json 

    const div_to_remove = document.getElementById("removeme"); // Removing the div that was used to import the json file
    div_to_remove.remove();
    document.title = intern[0].content; // Sets the title of the page to the title of the article

      intern.forEach(dict => { // Loop through the json file
        addElement(dict); // Display the content of the json file
      });
            };
    fileread.readAsText(file_to_read);
}

function addElement(dict) {
    var newDiv = document.createElement("div"); // Create a new <div> element
    var newContent = document.createTextNode(dict.content); // Create a text node

    if (dict.class == "image") {
        var newImg = document.createElement("img"); // Create a new <img> element
        newImg.src = dict.source; // Set the source of the image
        newDiv.appendChild(newImg); // Append the image to the <div>
    }
    
    newDiv.appendChild(newContent); // Append the text to <div>
    newDiv.classList.add(dict.class); // Add the class to the <div>
    container.insertBefore(newDiv, footer); // Append <div> to the HTML document, in the container and before the footer
}

document.getElementById("jsonfileinput").addEventListener("change", getJsonFile);