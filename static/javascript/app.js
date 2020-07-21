const typedTextSpan  = document.querySelector('.typed-text')
const cursorSpan = document.querySelector(".cursor")
var collapse = document.querySelectorAll("button.collapse");
var darkElement = document.querySelector(".dark-mode")

const textArray = ["easy", "fun", "free", "life", "best"]
const typingDelay = 200;
const erasingDelay = 100;
const newTextDelay = 2000;
let textArrayIndex = 0;
let charIndex = 0;


function dark(){
    var element = document.body;
    element.classList.toggle("dark-mode");
}


for(var i = 0;i<collapse.length;i++){
    collapse[i].onclick = function(){
        this.classList.toggle("active");
        this.nextElementSibling.classList.toggle('show');
   }
}


function type(){
    if(charIndex < textArray[textArrayIndex].length){
        if(!cursorSpan.classList.contains("typing")) cursorSpan.classList.add("typing")
        typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, typingDelay);
    } else{
        cursorSpan.classList.remove("typing")
        setTimeout(erase, newTextDelay);
    }

}

function erase(){
    if(charIndex > 0){
        if(!cursorSpan.classList.contains("typing")) cursorSpan.classList.add("typing")

        typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex-1);
        charIndex--;
        setTimeout(erase, erasingDelay);
    } else {

        cursorSpan.classList.remove("typing")

        textArrayIndex++;
        if(textArrayIndex>=textArray.length) textArrayIndex=0;
        setTimeout(type, typingDelay + 1100);
    }
}

document.addEventListener("DOMContentLoaded", function(){
    setTimeout(type, newTextDelay + 250);
});


