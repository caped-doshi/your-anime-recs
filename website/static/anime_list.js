console.log('loaded anime list');

const anime_list = document.getElementById("anime_list");
const search_bar = document.getElementById("searchBar");
let anime = [];
let ratings = [];
let anime_details = [];

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

async function fetch_anime (){
    search_bar.disabled = true;
    console.log("fetching anime");
    let response = await fetch('/get_anime_list',{method:"POST"});
    let data = await response.json();
    return data;
}

async function fetch_rating (anime_name){
    console.log("fetching rating");
    let response = await fetch('/get_rating',{method:"POST"});
    let data = await response.json();
    return data;
}

async function fetch_anime_details(){
    console.log("fetching details");
    let response = await fetch('/get_anime_details',{method:"POST"});
    let data = await response.json();
    return data;
}

async function load_anime (search) {
    //make this async function that loads from mongodb cloud 
    anime = await fetch_anime();
    ratings = await fetch_rating();
    anime_details = await fetch_anime_details();
    console.log(anime_details);
    search_bar.disabled=false;
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
            let details = anime_details[a];
            return `
            <form id=${"jsform_"+c} method="POST">
                <li class='list-group-item list-group-item-action' id="${a}">
                    <h6 value="${search}" >${a}</h6>
                    <h6>${details[0]}/10 on IMDB</h6>
                    <input type="hidden" name="search_bar" value=${search}></input>
                    <img src="${details[2]}"></img>
                    <p>${details[1]}</p>
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
                    <button type="button" id=${"btn_"+c} class="btn btn-primary">Rate</button>
                    <input type="hidden" id="name" name="name" value="${a}"></input>
                    <input type="hidden" id="${"rating_"+a}" name="${"rating_"+a}" value="0"></input>
                </li>
            </form>
            `;
        }).join('');
        //onClick=\"getRating(${c}, \"${a}\")\"
        anime_list.innerHTML = html_string;
        for(let a = 0; a < anime.length; a++){
            let temp_button = "btn_"+(a+1);
            document.getElementById(temp_button).addEventListener('click', function(){
                console.log(temp_button);
                getRating(a+1, anime[a]);
            });
            if(anime[a] in ratings){
                let temp_rating = ratings[anime[a]];
                console.log(anime[a]);
                console.log(temp_rating);
                let temp_id = "star" + temp_rating+"_"+(a+1);
                console.log(temp_id);
                document.getElementById(temp_id).checked = true;
            }
        };
    };
};

function getRating(r, a) {
    console.log('getting rating');
    var ele = document.getElementsByTagName("input");
    var max = 0;
    var name = "rating_" + r;
    var rating_count = 0;
    for (var i = 0; i < ele.length; i++){
        if(ele[i].type === "radio" && ele[i].name === name){
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
    load_anime();
};

load_anime();

filter(anime, search_bar.value);



