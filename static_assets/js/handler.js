(function ($) {
    var $document = $(document);

    if (!History.enabled) {
        return false;
    }

    var root = History.getRootUrl();

    $.expr.filters.internal = function (elem) {
        return (elem.hostname == window.location.hostname && /(\/|\.html)$/i.test(elem.pathname)) || false;
    };

    function find_all($html, selector) {
        return $html.filter(selector).add($html.find(selector));
    }

    function parse_html(html) {
        return $($.parseHTML(html, document, true));
    }

    function parse_response(html) {
        var
        head = /<head[^>]*>([\s\S]+)<\/head>/.exec(html),
        body = /<body[^>]*>([\s\S]+)<\/body>/.exec(html),

        $head = head ? parse_html(head[1]) : $(),
        $body = body ? parse_html(body[1]) : $(),

        title = $.trim(find_all($head, 'title').last().html()),
        $content = $.trim(find_all($body, '#content').first().html());

        return {
            'title': title,
            '$content': $content
        }
    }

    $document.ready(function () {
        // initialize stuff here as needed

        $document.on('click', 'a:internal', function (event) {
            if (event.which == 2 || event.ctrlKey || event.metaKey) {
                return true;
            }

            History.pushState(null, null, $(this).attr('href'));
            event.preventDefault();

            return false;
        });
    });

    $(window).on('statechange', function () {
        var
        url = History.getState().url,
        rel = url.replace(root, '/');

        $.get(rel).done(function (date) {
            var response = parse_response(date);

            if (!response.$content.length) {
                document.location.href = url;

                return false;
            }

            var $content = $('#content');

            if (response.title.length) {
                $('title').last().html(response.title);
            }

            $content
            .fadeOut(500)
            .promise()
            .done(function () {
                $content.html(response.$content).fadeIn(500);
                // initialize stuff here as needed
            });
        }).fail(function () {
            document.location.href = url;

            return false;
        });
    });
})(jQuery);
