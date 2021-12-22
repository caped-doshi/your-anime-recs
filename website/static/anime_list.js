console.log('loaded anime list');

const anime_list = document.getElementById("anime_list");
const search_bar = document.getElementById("searchBar");
let anime = [];

search_bar.addEventListener('keyup', (e) => {
    console.log('keyup');
    let search = e.target.value.toLowerCase();
    const filtered = anime.filter((a) => {
        return a.toLowerCase().includes(search);
    });
    display_anime(filtered, search);
});

const filter = (arr, search) => {
    console.log(search);
    search = search.toLowerCase();
    const filtered = arr.filter((a)=>{
        return a.toLowerCase().includes(search);
    });
    console.log('filter');
    console.log(filtered);
    display_anime(filtered, search);
}

const load_anime = (search) => {
    //make this async function that loads from mongodb cloud 
    anime = ["Naruto", "One Piece", "Attack on Titan", "My Hero Academia", "Hunter X Hunter"];
};

const display_anime = (anime, search) => {
    if(search !== ""){
        const html_string = anime.map((a) => {
            const a_string = a;
            return `
            <form method="POST">
                <li class='list-group-item list-group-item-action' id="${a}">
                    <h6 value="${search}" >${a}</h6>
                    <input type="hidden" name="search_bar" value=${search}></input>
                    <textarea name="rating" id="rating" class="form-control"></textarea>
                    <button type="submit" class="btn btn-primary" name="name" value="${a}">Rate</button>
                </li>
            </form>
            `;
        }).join('');
        anime_list.innerHTML = html_string;
    };
};

load_anime();
filter(anime, search_bar.value);