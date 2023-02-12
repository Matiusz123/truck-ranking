
let refresh = document.querySelectorAll('#refresh');
    refresh.forEach(function (ele){
          ele.addEventListener('click',function (event){
              ele.style.backgroundColor = 'lightblue'
            setTimeout(function() {
                ele.style.backgroundColor = 'white'
                }, 10000);

          })
            })