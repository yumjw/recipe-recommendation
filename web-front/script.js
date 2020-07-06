const typeEl = document.getElementById('type')
const addBtn = document.getElementById('add')
const resulttitle = document.querySelector('.resulttitle')
const ingredientUl = document.getElementById('ingredient-ul')
const notification = document.getElementById('notify')
const submitBtn = document.getElementById('submit')
const resultContainer = document.getElementById('result-container')


const loader = document.getElementById('loader')

loader.style.display = 'none';

//엔터치면 추가 클릭
typeEl.addEventListener('keydown', (e) => {
    if (e.key == 'Enter') {
        addBtn.click()
    }
})


//추가버튼 누르면 재료 들어감
addBtn.addEventListener('click', () => {
    const text = typeEl.value;
    if (text === "") return

    notification.innerHTML = ""

    if (!inglist.includes(text)) {
        notification.innerHTML = '없는 재료입니다!'

    } else {
        ingredientUl.innerHTML += `<li class="ingredient">${text}<button class="delete">x</button></li>`
    }
    typeEl.value = ''
})


ingredientUl.addEventListener('click', (e) => {
    if (e.target.classList.contains('delete')) {
        e.target.closest('li').remove()
    } else if (e.target.classList.contains('ingredient')) {
        e.target.classList.toggle('active')
    }

})


submitBtn.addEventListener('click', (e) => {
            var send_must = [];
            var send_option = [];
            const ingredientLists = ingredientUl.children
            for (let i = 0; i < ingredientLists.length; i++) {
                var arrValue = ingredientLists[i].textContent.slice(0, -1);
                if (ingredientLists[i].classList.contains('active')) {
                    send_must.push(arrValue)
                } else {
                    send_option.push(arrValue)
                }
            }
            resultContainer.innerHTML = ''
            loader.style.display = 'block'

            fetch(`http://3.133.76.141:10001/plus?user_musts=[${send_must.map(x=> `"${x}"`)}]&user_options=[${send_option.map(x=>`"${x}"`)}]`)
            .then(res => {return res.json()})
            .then(datalist => {
                loader.style.display='none'

                if(Object.keys(datalist).length===0){
                    resultContainer.innerHTML='<div></div><img src="https://1.gall-img.com/hygall/files/attach/images/82/338/473/273/c2acce0288e9e105d72e0ecab5aa99a8.jpg">'
                    return
                }
                resultContainer.innerHTML = `<h1 class="resulttitle" id="resulttitle">레시피 결과</h1>
                <div class="result" id='result'>

                </div>`
                const result = document.getElementById('result')
                for (let data in datalist){
                result.innerHTML += `
                <div class="rec">
                    <a href="${datalist[data].recipe_url}"><img src="${datalist[data].image_url}" alt="image">
                    </a>
                    <p class="title">${datalist[data].title}</p>
                    <div class="idonthave">&#x274C${datalist[data].required_ingredients}</div>
                </div>`
                }

                location.href = "#result-container"
            })
            .catch(err=>{return console.log(err)})
    

    console.log(send_must, send_option)


})