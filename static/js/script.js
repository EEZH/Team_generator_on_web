const inputSearch = document.getElementById('input-search')
const listUsers = document.getElementById('list-users')
const cardHolder = document.getElementById('card-holder')

function renderUser(user){
    const cardHtml = `<div class="ui card">
                           <div class="content">
                                <span class="header">${user.name}</span>
                                <div class="meta">
                                    <span class="date">Speed: ${user.speed}</span>
                                </div>
//                                <div class="description">
//                                    ${user.shot}
//                                </div>
//                            </div>
//                            <div class="extra content">
//                                <a>${user.amplua}</a>
//                            </div>
                        </div>`
    cardHolder.innerHTML = cardHtml
}

function renderUserList(users){
    let usersHtml = ''

    for(let i = 0; i < users.length; i++){
        const user = users[i]

        const userHtml = `
        <li class="item" onclick="fetchUser(${user.id}, '${user.name}')">${user.name}</li>`

        usersHtml += userHtml
    }

    listUsers.innerHTML = usersHtml
}



function fetchUser(user_id, user_name){
    const url = `/player_stats?user_id=${user_id}&user_name=${user_name}`
    fetch(url)
        .then(response => response.json())
        .then(user => {
        listUsers.innerHTML = ''
        inputSearch.value = ''
        return renderUser(user)})
}

inputSearch.addEventListener('input', function(event){
    const name = event.currentTarget.value.trim()
    if(name.length == ''){
    listUsers.innerHTML = ''
    return
    }

    const url = `/users?name=${name}`
    fetch(url)
        .then(function(response){
            return response.json()
        })
        .then(function(data){
            renderUserList(data.users)
        })
})