window.onload = function() {
    selection_changed("pro", true);
    selection_changed("con", true);
    update_arguments();
};

function update_arguments() {
    pro_select = document.getElementById("selected_pro");
    con_select = document.getElementById("selected_con");
    content_div = document.getElementById("arguments_div")

    content_div.innerHTML = "";

    if (pro_select.value === "None" || con_select.value === "None") {
        content_div.innerHTML = "";
        return;
    }
    $.get("/api/compare?pro="+pro_select.value+"&con="+con_select.value, function(data) {
        content_div.innerHTML += `
            <div class="panel panel-info">
                <div class="panel-heading">
                </div>
                <div class="panel-body">
                    <a href="/argument/add?pro=${pro_select.value}&con=${con_select.value}">Add new Argument for this selection</a>
                </div>
            </div>
        `;

        if (data.length === 0) {
            content_div.innerHTML += `
                <div class="panel panel-info">
                    <div class="panel-heading">
                    </div>
                        <div class="panel-body">No arguments for this selection (yet)</div>
                    </div>
            `;
            return;
        }
        data.forEach(arg => {
            type = "panel-info";
            edit = "";
            if (arg.type === "pro") {
                type = "panel-success";
            } else if (arg.type === "con") {
                type = "panel-danger";
            }
            if (arg.edit_link !== "") {
                edit = `<a href="${arg.edit_link}">edit</a>`;
            }
            content_div.innerHTML += `
                <div class="panel ${type}">
                    <div class="panel-heading">
                        <b>Pro ${arg.pro_product_name}</b>
                    </div>
                    <div class="panel-body">${arg.comment}</div>
                    <div class="panel-footer">
                    <div style="font-size: small; float:left;">
                        ${edit}
                    </div>
                    <div style="float:right; font-style: italic;">by ${arg.username_created} on ${arg.date_created_formatted}</div>
                    <div style="clear:both"></div>
                    </div>
                </div>
            `
        });
    });
};

function selection_changed(side, on_init=false) {
    selector = null;
    prod_content_div = null;
    if (side === "pro") {
        selector = document.getElementById("selected_pro");
        prod_content_div = document.getElementById("pro_product_div");
    } else if (side === "con") {
        selector = document.getElementById("selected_con");
        prod_content_div = document.getElementById("con_product_div");
    } else {
        return;
    }
    if (selector.value === "None") {
        prod_content_div.innerHTML = ""
        return;
    }
    $.ajax({
        type: "GET",
        url: "/api/products/" + selector.value,
        div: prod_content_div,
        success: function(data) {
            this.div.innerHTML = `
                <img src="data:image/png;base64,${data.image}" style="max-height:100px; max-width:200px;" />
                <h3>${data.name} (${data.company.name})</h3>
                <p style="font-weight:bold;">About ${data.company.name}</p>
                <p><span style="font-weight:bold;">Country:</span> ${data.company.country}</p>
                <p font-style="italic">${data.company.description}</p>
            `;
        }
    });

    if (!on_init) {
        update_arguments();
    }
};