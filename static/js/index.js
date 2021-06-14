var goldPrompt = document.getElementById("GoldPrompt");
var silverPrompt = document.getElementById("SilverPrompt");
var groceryPrompt = document.getElementById("GroceriePrompt");

// // set displays of prompts to none
// silverPrompt.style.display = "none";
// groceryPrompt.style.display = "none";

// Remove required attribute
function remReqGold(){
    document.getElementById("buySellGold1").removeAttribute("required");
    document.getElementById("buySellGold2").removeAttribute("required");
    document.getElementById("goldWeight").removeAttribute("required");
    document.getElementById("goldRate").removeAttribute("required");
};
function remReqSilver(){
    document.getElementById("buySellSilver1").removeAttribute("required");
    document.getElementById("buySellSilver2").removeAttribute("required");
    document.getElementById("silverWeight").removeAttribute("required");
    document.getElementById("silverRate").removeAttribute("required");
};
function remReqGroc(){
    document.getElementById("buySellGrocerie1").removeAttribute("required");
    document.getElementById("SubCatGrocerie").removeAttribute("required");
    document.getElementById("grocQuantity").removeAttribute("required");
    document.getElementById("grocRate").removeAttribute("required");  
};

// runs this func when clicked on category radios and sets their displays accordingly
function checkRadio () {
    if(document.getElementById("CatRadioGold").checked){
        goldPrompt.style.display = "block";
        silverPrompt.style.display = "none";
        groceryPrompt.style.display = "none";
        document.getElementById("buySellGold1").setAttribute("required", "");
        document.getElementById("buySellGold2").setAttribute("required", "");
        document.getElementById("goldWeight").setAttribute("required", "");
        document.getElementById("goldRate").setAttribute("required", "");
        remReqSilver();
        remReqGroc();
    }
    else if(document.getElementById("CatRadioSilver").checked){
        goldPrompt.style.display = "none";
        silverPrompt.style.display = "block";
        groceryPrompt.style.display = "none";
        document.getElementById("buySellSilver1").setAttribute("required", "");
        document.getElementById("buySellSilver2").setAttribute("required", "");
        document.getElementById("silverWeight").setAttribute("required", "");
        document.getElementById("silverRate").setAttribute("required", "");
        remReqGold();
        remReqGroc();
    }
    else if(document.getElementById("CatRadioGrocerie").checked){
        goldPrompt.style.display = "none";
        silverPrompt.style.display = "none";
        groceryPrompt.style.display = "block";
        document.getElementById("buySellGrocerie1").setAttribute("required", "");
        document.getElementById("SubCatGrocerie").setAttribute("required", "");
        document.getElementById("grocQuantity").setAttribute("required", "");
        document.getElementById("grocRate").setAttribute("required", "");
        remReqGold();
        remReqSilver();
    }
    else{
        return 0;
    }
};

