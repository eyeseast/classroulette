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

var ad = window.innerWidth > 768 ? ads.leaderboard : ads.banner
  , google_ad_client = ads.client
  , google_ad_slot   = ad.id
  , google_ad_width  = ad.width
  , google_ad_height = ad.height;