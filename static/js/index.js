var goldPrompt = document.getElementById("GoldPrompt");
var silverPrompt = document.getElementById("SilverPrompt");
var groceryPrompt = document.getElementById("GroceriePrompt");

// set displays of prompts to none
silverPrompt.style.display = "none";
groceryPrompt.style.display = "none";

// runs this func when clicked on category radios and sets their displays accordingly
function checkRadio () {
    if(document.getElementById("CatRadioGold").checked){
        goldPrompt.style.display = "block";
        silverPrompt.style.display = "none";
        groceryPrompt.style.display = "none";
    }
    else if(document.getElementById("CatRadioSilver").checked){
        goldPrompt.style.display = "none";
        silverPrompt.style.display = "block";
        groceryPrompt.style.display = "none";
    }
    else if(document.getElementById("CatRadioGrocerie").checked){
        goldPrompt.style.display = "none";
        silverPrompt.style.display = "none";
        groceryPrompt.style.display = "block";
    }
    else{
        return 0;
    }
};

