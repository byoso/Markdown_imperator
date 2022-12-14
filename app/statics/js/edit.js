
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      });
    }


    let history = []
    let history_index = 0
    let doc_id = {{ doc.id }}
    let title = document.getElementById('title')
    let content = document.getElementById('content')
    let render = document.getElementById('render')
    let render_sc = document.getElementById('render_sc')
    let save_button = document.getElementById('save_button')
    var save_url = "{{ url_for('edit', doc_id=doc.id) }}";
    let cats = {{ categories | safe}};
    let category_selection = document.getElementById('categories');

    history.push({'title': title.value, "content": content.value})
    history_index ++

    // Add the Categories checkboxes
    let catBoxes = []

    function insertAfter(newNode, referenceNode) {
        referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}
    function newCategoryBox(cat) {
        console.log(cat)
        let elem = document.createElement('input')
        elem.type = "checkbox"
        elem.name = cat.name
        elem.id = cat.id
        if (cat.is_checked) {
            elem.checked = true
        }
        return elem
    };
    function newCategoryLabel(cat) {
        let label = document.createElement('label')
        let toId = cat.id
        label.setAttribute("for", toId)
        label.innerHTML = cat.name
        return label
    };

    cats.forEach(cat => {
        let elem=  newCategoryBox(cat)
        elem.style = "margin-right: 10px;"
        category_selection.appendChild(elem)
        catBoxes.push(elem)
        let label = newCategoryLabel(cat)
        category_selection.appendChild(label)
        let lineBack = document.createElement("br")
        category_selection.appendChild(lineBack)
        console.log(cat.name)
    });

    render.innerHTML = marked.parse(content.value);

    // prevent links to open
    var links = render.getElementsByTagName('a')
    for (var i=0; i<links.length; i++){
        var link = links[i]
        links[i].addEventListener('click', event => {
            event.preventDefault();
        })
    }
    // realtime render update
    document.addEventListener('keyup', e => {
        render.innerHTML = marked.parse(content.value)+"<br>";
        }
    );

    // Animation
    function animation(id) {
        let elem = document.getElementById(id)
        elem.classList.remove('validate');
        void elem.offsetWidth;
        elem.classList.add('validate');
        }

    // copy to clipboard
    function toClipboard() {
        var copyText = document.getElementById("content");
        navigator.clipboard.writeText(copyText.value);
        animation("copy")
    }

    // save_button function
    save_button.addEventListener('click', e =>{
        if (history_index < history.length-1){
            history = history.slice(0, history_index)
        }
        animation("save_button")

        history.push({'title': title.value, "content": content.value})
        var headers = new Headers();
        var datas = new FormData();
        datas.append('title', title.value)
        datas.append('doc_id', doc_id)
        datas.append('content', content.value)
        categories = []
        catBoxes.forEach(elem => {
            categories.push([elem.id, elem.checked])
        })
        console.log(categories) // debug
        categories = JSON.stringify(categories)
        datas.append('categories', categories)

        console.log(datas)

        var requestOptions = {
        method: 'POST',
        headers: headers,
        body: datas,
        redirect: 'follow'
        };

        fetch(save_url, requestOptions)
        .then(response => response.text())
        // .then(result => console.log(result))
        .catch(error => console.log('error', error));

        history_index ++

        });

    // tab modification
    document.addEventListener('keydown', e => {
        if (e.key === "Tab") {
            e.preventDefault();
            let start = e.target.selectionStart;
            let val = e.target.value;
            e.target.value = val.substr(0, start) + "    " + val.substr(e.target.selectionEnd);
            e.target.selectionStart = e.target.selectionEnd = start + 4;
            // document.getElementById('save_button').click();
        }
    });

    // ctrl+s redirects to save_button function
    document.addEventListener('keydown', e => {
        if (e.ctrlKey && e.key ==='s') {
            e.preventDefault();
            document.getElementById('save_button').click();
        }
    });

    // ctrl+p
    document.addEventListener('keydown', e => {
        if (e.ctrlKey && e.key ==='p') {
            e.preventDefault();
            printer.innerHTML = render.innerHTML;
            document.getElementById('editor').style.display = 'none';
            document.getElementById('navbar').style.display = 'none';
            document.getElementById('render_sc').style.display = 'none';
            window.print();
            document.getElementById('navbar').style.display = 'block';
            document.getElementById('editor').style.display = 'block';
            document.getElementById('render_sc').style.display = 'block';
            printer.innerHTML = "";
        }
    });

    // ctrl+z
    document.addEventListener('keydown', e => {
        if (e.ctrlKey && e.key ==='z') {
            e.preventDefault();
            if (history_index - 1 >= 0) {
                title.value = history[history_index-1]['title']
                content.value = history[history_index-1]['content']
                history_index --
            }
        }
    });

    // ctrl+y
    document.addEventListener('keydown', e => {
        if (e.ctrlKey && e.key ==='y') {
            e.preventDefault();
            if (history_index < history.length) {
                title.value = history[history_index+1]['title']
                content.value = history[history_index+1]['content']
                history_index ++
            }
        }
    });

    // scrollbars synchro
    function syncScroll(scroller) {
    let render_height = render_sc.scrollHeight
    let render_pos = render_sc.scrollTop
    let render_frame = render_sc.offsetHeight
    let content_height = content.scrollHeight
    let content_pos = content.scrollTop
    let content_frame = content.offsetHeight
    if (scroller.id == "content") {
        var pos = (content_pos + content_frame)*render_height/content_height-render_frame
        render_sc.scrollTo(0, pos);
        let ratio = content
        console.log(content_pos + " / " + content_height + " - " + content_frame)
    }
    }
