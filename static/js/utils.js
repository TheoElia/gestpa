function exists(ele){
    if (ele !== null && ele !== undefined){
        return true;
    } else {
        return false;
    }
}

function buildForm(id){
    let myForm = document.getElementById(id);
    let formData = new FormData(myForm);
    var obj = {};
    for(var pair of formData.entries()){
        var name = pair[0];
        var val = pair[1];
        obj[name] = val;
    }
    return obj;
}

function removeObjectFromArray(array, obj) {
    const index = array.findIndex(item => {
        return Object.keys(obj).every(key => obj[key] === item[key]);
    });
    if (index !== -1) {
        array.splice(index, 1);
    }
    return array;
}

function generateRandomString() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const charactersLength = characters.length;
    for (let i = 0; i < 6; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function buildFormArray(id){
    let myForm = document.getElementById(id);
    let formData = new FormData(myForm);
    var currentId = multiFormFirstId;
    var all = [];
    var obj = {};
    var reservedObj = {};
    for(var pair of formData.entries()){
        var idToRemove = pair[0].split("-")[1];
        var name = pair[0].replace(idToRemove,"").replace("-","");
        var val = pair[1];
        if(exists(idToRemove)){
            if(idToRemove == currentId){
                obj[name] = val;
                currentId = idToRemove;
            } else {
                all.push({...obj, ...reservedObj});
                obj = {};
                obj[name] = val;
                currentId = idToRemove;
            }
        } else {
            reservedObj[name] = val;
        }
    }
    all.push({...obj, ...reservedObj});
    return all;
}


function show_the_numbers(string){
    return string.match(/[0-9]+/g);
}

function convertDate(dateStr) {
    // Split the input date string by '/'
    const [day, month, year] = dateStr.split('/');
    
    // Format the date as yyyy-mm-dd
    const formattedDate = `${year}-${month}-${day}`;
    
    return formattedDate;
}

function convertNormalDate(dateStr) {
    // Split the input date string by '/'
    const [year, month, day] = dateStr.split('-');
    
    // Format the date as yyyy-mm-dd
    const formattedDate = `${year}-${month}-${day}`;
    
    return formattedDate;
}

function toast(msg,time) {
    var x = document.getElementById("toast");
    x.innerHTML = msg;
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, time);
    return true
  }


function setFieldValue(id,value){
    if(exists(value)){
        $("#"+id).val(value);
    }
}