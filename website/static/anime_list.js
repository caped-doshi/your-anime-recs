console.log('loaded anime list');

const anime_list = document.getElementById("anime_list");
const search_bar = document.getElementById("searchBar");
let anime = [];

search_bar.addEventListener('keyup', (e) => {
    console.log('keyup');
    const search = e.target.value.toLowerCase();
    const filtered = anime.filter((a) => {
        return a.toLowerCase().includes(search);
    });
    display_anime(filtered);
});

const load_anime = () => {
    anime = ["Naruto", "One Piece", "Attack on Titan", "My Hero Academia", "Hunter X Hunter"];
    console.log(anime);
};

const display_anime = (anime) => {
    const html_string = anime.map((a) => {
        console.log('loop')
        return `
            <li class="anime">
                <h6>${a}</h6>
            </li>
        `;
    }).join('');
    anime_list.innerHTML = html_string;
};

load_anime();