function desbloqueo(){
    var switch1 = document.getElementById("nombre").disabled;
    if (switch1){
        document.getElementById("nombre").disabled = false;
        document.getElementById("username").disabled = false;
    }
    else{
        document.getElementById("nombre").disabled = true;
        document.getElementById("username").disabled = true;
    }
}