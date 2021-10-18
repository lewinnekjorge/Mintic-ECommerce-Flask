const formulario = document.getElementById("FormConta");
const nombre = document.getElementById("formnombre");
const correo = document.getElementById("formemail");
const asunt = document.getElementById("formasunto");
const mensaj = document.getElementById("formmensaje");
const parrafo = document.getElementById("warnings")
const parrafo1 = document.getElementById("warnings1")
const parrafo2 = document.getElementById("warnings2")
const parrafo3 = document.getElementById("warnings3")


formulario.addEventListener("submit", e =>{
    e.preventDefault()
    let warnings = ""
    let warnings1 = ""
    let warnings2 = ""
    let warnings3 = ""
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/
    let entrar = false
    if(nombre.value.length <6){
        warnings += `El nombre es muy corto <br>`
        entrar = true
    }
    if(!regexEmail.test(correo.value)){
        warnings1 += `El email no es valido <br>`
        entrar = true
    }
    if(asunt.value.length <8){
        warnings2 += `Indique su Asunto <br>`
        entrar = true
    }
    if(mensaj.value.length <7){
        warnings3 += `El campo mensaje no debe estar vacio. <br>`
        entrar = true
    }

    if(entrar){
        parrafo.innerHTML = warnings
        parrafo1.innerHTML = warnings1
        parrafo2.innerHTML = warnings2
        parrafo3.innerHTML = warnings3
        
    }else{
        alert("enviado")
        formulario.reset();
    }
})
