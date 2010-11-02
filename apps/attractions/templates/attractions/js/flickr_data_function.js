function(data){
    // append each photo to a li
    $.each(data.items, function(i, item) {
        i = i++;
        $('<img alt=""/>').attr("src",
        item.media.m).attr("title", item.title).appendTo("ul.flickr").wrap('<li><a href="' + item.media.m + '" rel="group"  title="' + item.title + '"></a></li>');
        // convert to small thumb
        $("ul.flickr li a img").each(function() {
            var smallThumb = $(this).attr("src").replace(/_m.jpg$/i,'_s.jpg'); 
            $(this).attr("src", smallThumb);
        });
        // modify to regular image size
        $("ul.flickr li a").each(function() {
            var modURL = $(this).attr("href").replace(/_m.jpg$/i,'.jpg');
            $(this).attr("href", modURL);

            $(this).fancybox({                                                                                                                
                'titleShow' : true,
                'titlePostion': 'outside',
                'cyclic': true,
                'showNavArrows': true
            });
        });
        if(i==11) return false;    
    });
}
