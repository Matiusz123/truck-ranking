let a = document.querySelectorAll('#przyciski a')

a.forEach(function (ele){
    ele.addEventListener('mouseover',function (){
        this.style.backgroundColor = 'lightblue';
    })
    ele.addEventListener('mouseout',function (){
        this.style.backgroundColor = 'lightgrey';
    })
})