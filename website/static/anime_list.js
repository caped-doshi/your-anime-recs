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
    if (search === ""){
        anime_list.innerHTML ='';
    };
    if(search !== ""){
        var c = 0;
        const html_string = anime.map((a) => {
            c = c + 1;
            const a_string = a;
            let r = "rating_" + c;
            return `
            <form id=${"jsform_"+c} method="POST">
                <li class='list-group-item list-group-item-action' id="${a}">
                    <h6 value="${search}" >${a}</h6>
                    <input type="hidden" name="search_bar" value=${search}></input>
                    <div class="rate">
                        <input type="radio" id=${"star5_"+c} name=${r} value="5" />
                        <label for=${"star5_"+c} title="text">5 stars</label>
                        <input type="radio" id=${"star4_"+c} name=${r} value="4" />
                        <label for=${"star4_"+c} title="text">4 stars</label>
                        <input type="radio" id=${"star3_"+c} name=${r} value="3" />
                        <label for=${"star3_"+c} title="text">3 stars</label>
                        <input type="radio" id=${"star2_"+c} name=${r} value="2" />
                        <label for=${"star2_"+c} title="text">2 stars</label>
                        <input type="radio" id=${"star1_"+c} name=${r} value="1" />
                        <label for=${"star1_"+c} title="text">1 star</label>
                    </div>
                    <button type="button" class="btn btn-primary" onClick="getRating(${c}, '${a}')">Rate</button>
                    <input type="hidden" id="name" name="name" value="${a}"></input>
                    <input type="hidden" id="${"rating_"+a}" name="${"rating_"+a}" value="0"></input>
                </li>
            </form>
            `;
        }).join('');
        anime_list.innerHTML = html_string;
    };
};

function getRating(r, a) {
    var ele = document.getElementsByTagName("input");
    var max = 0;
    var name = "rating_" + r;
    var rating_count = 0;
    for (var i = 0; i < ele.length; i++){
        if(ele[i].type === "radio" && ele[i].name == name){
            rating_count+=1;
            console.log(ele[i].id);
            if(ele[i].checked){
                max = 6 - rating_count;
                console.log(max);
            }
        }
    };
    let temp = "rating_" + a;
    console.log(temp);
    document.getElementById(temp).value = max;
    document.getElementById('jsform_'+r).submit();
};

load_anime();
filter(anime, search_bar.value);



