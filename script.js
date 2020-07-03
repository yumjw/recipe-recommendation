const typeEl = document.getElementById('type')
const addBtn = document.getElementById('add')

const ingredientUl = document.getElementById('ingredient-ul')
const notification = document.getElementById('notify')
const submitBtn = document.getElementById('submit')
const result = document.querySelector('.result')
const recimg = document.getElementsByTagName('img')

const ing_inbox = document.getElementsByClassName('ingredient');
// const ing_must = document.g


//엔터치면 추가 클릭
typeEl.addEventListener('keydown', (e) => {
    if (e.key == 'Enter') {
        addBtn.click()
    }
})

// new autoComplete({
//     selector: typeEl,
//     minChar: 1,
//     source: function(term, suggest) {
//         const matches = inglist.filter(ing => {
//             return ing.includes(term)
//         })
//         suggest(matches)
//     }
// })

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

            fetch(`https://3.133.76.141:8000/plus?user_musts=[${send_must.map(x=> `"${x}"`)}]&user_options=[${send_option.map(x=>`"${x}"`)}]`)
            .then(res => {return res.json()})
            .then(datalist => {
                console.log(datalist)
                for (let data in datalist){
                result.innerHTML += `
                <div class="rec">
                    <a href="${datalist[data].recipe_url}"><img src="${datalist[data].image_url}" alt="image">
                    </a>
                    <div class="title">${datalist[data].title}</div>
                    <div class="idonthave">&#x274C${datalist[data].required_ingredients}</div>
                </div>`
                }
            })
            .catch(err=>{return console.log(err)})
    

    console.log(send_must, send_option)

    //post로 어떻게 던지는가.......?


})

//임시 이케 나왔다 치고


//['6935188', '6847884', '6854893', '6912734', '6899265', '6846148'];