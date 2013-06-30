/***
<ins class="adsbygoogle"
     style="display:inline-block;width:728px;height:90px"
     data-ad-client="ca-pub-1794168544677954"
     data-ad-slot="4723846917"></ins>
***/
var adsbygoogle;
document.addEventListener('DOMContentLoaded', showAds);

function showAds(e) {
    var ads = {

        client: "ca-pub-1794168544677954",
        
        leaderboard: {
            id: 4723846917,
            height: '90px',
            width: '728px'
        },

        banner: {
            id: 3474112912,
            height: '50px',
            width: '320px'
        }
    };

    var ins = document.createElement('ins')
      , ad = window.innerWidth > 768 ? ads.leaderboard : ads.banner
      , container = document.getElementById('ad1');

    ins.setAttribute('data-ad-client', ads.client);
    ins.setAttribute('data-ad-slot', ad.id);
    ins.style.display = "inline-block";
    ins.style.height = ad.height;
    ins.style.width = ad.width;

    container.appendChild(ins);

    (adsbygoogle = window.adsbygoogle || []).push({});

}