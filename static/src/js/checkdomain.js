function remove_hide_btn_view(view_type)
{
    if(view_type === 'multi')
    {
        $('#single_domain_area').addClass('d-none');
        $('#multi_domain_area_input').removeClass('d-none');
        $('#multi_domain_area_btn').removeClass('d-none');
    }
    else
    {
        $('#single_domain_area').removeClass('d-none');
        $('#multi_domain_area_input').addClass('d-none');
        $('#multi_domain_area_btn').addClass('d-none');
    }
    $('.sheetjs_export_excel').addClass('d-none');
}

function rdap_custom_data()
{
    return {
        registrar: '',
        registrar_url: '',
        domain_status: [],
        nameservers: [],
        creation_date: '',
        updated_date: '',
        expiry_date: '',
        verified: false
    }
}

function rdap_parse_data(data)
{
    var result = rdap_custom_data();
    if(!jQuery.isEmptyObject(data))
    {
        if('status' in data && data.status && data.status.length > 0)
        {
            result.domain_status = data.status;
        }
        if('nameservers' in data && data.nameservers && data.nameservers.length > 0)
        {
            var nameservers = [];
            for (let i = 0; i < data.nameservers.length; ++i)
            {
                if('ldhName' in data.nameservers[i])
                {
                    nameservers.push(data.nameservers[i]['ldhName']);
                }
            }
            result.nameservers = nameservers;
        }
        if('events' in data && data.events && data.events.length > 0)
        {
            for (let i = 0; i < data.events.length; ++i)
            {
                if('eventAction' in data.events[i] && 'eventDate' in data.events[i])
                {
                    if(data.events[i].eventAction === 'registration')
                    {
                        result.creation_date = data.events[i].eventDate;
                    }
                    if(data.events[i].eventAction === 'last changed')
                    {
                        result.updated_date = data.events[i].eventDate;
                    }
                    if(data.events[i].eventAction === 'expiration')
                    {
                        result.expiry_date = data.events[i].eventDate;
                    }
                }
            }
        }
        if('entities' in data && data.entities && data.entities.length > 0)
        {
            for (let i = 0; i < data.entities.length; ++i)
            {
                let entities = data.entities[i];
                if('url' in entities)
                {
                    result.registrar_url = entities.url;
                }

                if('objectClassName' in entities && 'roles' in entities &&
                    entities.roles.length >= 1 && entities.roles[0] === 'registrar')
                {
                    if('vcardArray' in entities && entities.vcardArray.length == 2)
                    {
                        let vcardArray = entities.vcardArray[1];
                        for (let j = 0; j < vcardArray.length; ++j)
                        {
                            if(vcardArray[j].length == 4)
                            {
                                if(!result.registrar && (vcardArray[j][0] === 'fn' || vcardArray[j][0] === 'org'))
                                {
                                    result.registrar = vcardArray[j][3];
                                }
                                if(!result.registrar_url && vcardArray[j][0] === 'url')
                                {
                                    result.registrar_url = vcardArray[j][3];
                                }
                            }
                        }
                    }
                    else if ('handle' in entities && entities.handle)
                    {
                        // RDAP nic.cz
                        result.registrar = entities.handle;
                    }
                    
                }

                if(result.registrar_url.length == 0 && 'entities' in entities && entities.entities.length > 0)
                {
                    let entities_item = entities.entities;
                    for (let i = 0; i < entities.entities.length; ++i)
                    {
                        if('vcardArray' in entities_item[i] && entities_item[i].vcardArray.length > 0)
                        {
                            if('vcardArray' in entities_item[i] && entities_item[i].vcardArray.length == 2)
                            {
                                let entities_item_vcard = entities_item[i].vcardArray[1];
                                for (let j = 0; j < entities_item_vcard.length; ++j)
                                {
                                    if(entities_item_vcard[j].length == 4 && entities_item_vcard[j][0] === 'email')
                                    {
                                        let email = entities_item_vcard[j][3];
                                        if(email.indexOf('@') > -1)
                                        {
                                            result.registrar_url = email.substring(email.length, email.indexOf('@') + 1);
                                        }
                                    }
                                }
                            }
                            
                        }
                    }
                }
            }
        }
    }
    return result;
}

function render_status_view(data)
{
    var render_status = '';
    for (let i = 0; i < data.domain_status.length; ++i)
    {
        let class_input_red = '';
        let item_status = data.domain_status[i];
        if(typeof(item_status) === 'string' && item_status.length > 0)
        {
            item_status = item_status.toLowerCase()
            if((item_status.indexOf('pending') > -1 && item_status.indexOf('delete') > -1 && item_status.indexOf('delete') > item_status.indexOf('pending'))
                || (item_status.indexOf('autorenewperiod') > -1) || (item_status.indexOf('auto renew period') > -1))
            {
                class_input_red = ' is-invalid';
            }
        }
        render_status = render_status + `<input type="text" class="form-control${class_input_red}" value="${data.domain_status[i]}">`;
    }
    if(data.domain_status.length === 0)
    {
        render_status = `<input type="text" class="form-control" value="">`;
    }
    return render_status;
}

function rdap_render_view(domain, data, uuid)
{
    if(domain.indexOf('xn--') > -1)
    {
        // convert ASCII To Unicode
        domain = punycode.toUnicode(domain);
    }
    var render_status = render_status_view(data);

    var clipboard = `
        <a class="btn btn-icon btn_check_domain_clipboard" aria-label="Button">
            <!-- Download SVG icon from http://tabler-icons.io/i/search -->
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icons-card-icon icon-tabler icon-tabler-files" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M15 3v4a1 1 0 0 0 1 1h4">
                </path>
                <path d="M18 17h-7a2 2 0 0 1-2-2v-10a2 2 0 0 1 2-2h4l5 5v7a2 2 0 0 1-2 2z">
                </path>
                <path d="M16 17v2a2 2 0 0 1-2 2h-7a2 2 0 0 1-2-2v-10a2 2 0 0 1 2-2h2">
                </path>
            </svg>
        </a>
    `;

    var arr_render_data = [
        {
            id: 'input_registrar',
            label: 'Registrar:',
            data: data.registrar
        },
        {
            id: 'input_registrar_url',
            label: 'Registrar URL:',
            data: data.registrar_url
        },
        {
            id: 'input_creation_date',
            label: 'Creation Date:',
            data: data.creation_date
        },
        {
            id: 'input_updated_date',
            label: 'Updated Date:',
            data: data.updated_date
        },
        {
            id: 'input_expiry_date',
            label: 'Registry Expiry Date:',
            data: data.expiry_date
        }
    ];
    var render_info = '';
    arr_render_data.forEach(function(item_data, index)
    {
        render_info = render_info.concat(`
            <div class="mb-1 row">
                <label class="col-4 col-form-label">${item_data.label}</label>
                <div class="col input-group">
                    <input id="${item_data.id}" type="text" class="form-control" value="${item_data.data}">
                    ${clipboard}
                </div>
            </div>
        \n`);
    });
    var render = `
        <div id="${uuid}" class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 check_domain_result_area">
            <div class="card">
                <div class="card-body" style="padding-bottom: 0.25rem !important;">
                    <label id="label_domain" class="form-label fs-1" style="display: flex;justify-content: center;">${domain}</label>
                    ${render_info}
                    <div class="mb-1 row">
                        <label class="col-4 col-form-label">Domain Status:</label>
                        <div class="col input-group">
                            <div class="card check_domain_whois_status_area">
                                ${render_status}
                            </div>
                            
                        </div>
                    </div>

                    <div class="card-footer">
                        <div class="d-none check_domain_whois_data_no_progress">
                            <pre class="check_domain_whois_data_area">
                            </pre>
                        </div>
                        <div class="text-center check_domain_whois_data_progress">
                            <div class="text-secondary mb-3">WHOIS Query!!!</div>
                            <div class="progress progress-sm">
                                <div class="progress-bar progress-bar-indeterminate"></div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    `;
    return render;
}

function re_render_view(data, uuid, is_rdap)
{
    // Use whois data to fill some inputs
    var query_input_registrar = $('#' + uuid).find('#input_registrar');
    if(!query_input_registrar.attr('value'))
    {
        query_input_registrar.attr('value', data.parse.registrar);
    }
    
    var query_input_registrar_url = $('#' + uuid).find('#input_registrar_url');
    if(!query_input_registrar_url.attr('value'))
    {
        query_input_registrar_url.attr('value', data.parse.registrar_url);
    }
    
    var query_input_creation_date = $('#' + uuid).find('#input_creation_date');
    if(!query_input_creation_date.attr('value'))
    {
        query_input_creation_date.attr('value', data.parse.creation_date);
    }
    
    var query_input_updated_date = $('#' + uuid).find('#input_updated_date');
    if(!query_input_updated_date.attr('value'))
    {
        query_input_updated_date.attr('value', data.parse.updated_date);
    }
    
    var query_input_expiry_date = $('#' + uuid).find('#input_expiry_date');
    if(!query_input_expiry_date.attr('value'))
    {
        query_input_expiry_date.attr('value', data.parse.expiry_date);
    }
    
    if(data.parse.verified)
    {
        $('#' + uuid).find('#label_domain').append(
            `
                <svg viewBox="0 0 24 24" width="20" height="20" style="margin-top: 0.5rem; margin-left: 0.25rem;">
                    <path d="M12.3 2.9c.1.1.2.1.3.2.7.6 1.3 1.1 2 1.7.3.2.6.4.9.4.9.1 1.7.2 2.6.2.5 0 .6.1.7.7.1.9.1 1.8.2 2.6 0 .4.2.7.4 1 .6.7 1.1 1.3 1.7 2 .3.4.3.5 0 .8-.5.6-1.1 1.3-1.6 1.9-.3.3-.5.7-.5 1.2-.1.8-.2 1.7-.2 2.5 0 .4-.2.5-.6.6-.8 0-1.6.1-2.5.2-.5 0-1 .2-1.4.5-.6.5-1.3 1.1-1.9 1.6-.3.3-.5.3-.8 0-.7-.6-1.4-1.2-2-1.8-.3-.2-.6-.4-.9-.4-.9-.1-1.8-.2-2.7-.2-.4 0-.5-.2-.6-.5 0-.9-.1-1.7-.2-2.6 0-.4-.2-.8-.4-1.1-.6-.6-1.1-1.3-1.6-2-.4-.4-.3-.5 0-1 .6-.6 1.1-1.3 1.7-1.9.3-.3.4-.6.4-1 0-.8.1-1.6.2-2.5 0-.5.1-.6.6-.6.9-.1 1.7-.1 2.6-.2.4 0 .7-.2 1-.4.7-.6 1.4-1.2 2.1-1.7.1-.2.3-.3.5-.2z" fill="#3390ec"></path>
                    <path d="M16.4 10.1l-.2.2-5.4 5.4c-.1.1-.2.2-.4 0l-2.6-2.6c-.2-.2-.1-.3 0-.4.2-.2.5-.6.7-.6.3 0 .5.4.7.6l1.1 1.1c.2.2.3.2.5 0l4.3-4.3c.2-.2.4-.3.6 0 .1.2.3.3.4.5.2 0 .3.1.3.1z" fill="#fff"></path>
                </svg>
            `
        );
    }

    var arr_rdap_status = new Array();
    $('#' + uuid).find('.check_domain_whois_status_area > input').each(function() {
        var input = $(this);
        var val = input.val();
        if(typeof val === "string" && val.length > 0)
        {
            arr_rdap_status.push(val);
        }
    });
    if(arr_rdap_status.length == 0)
    {
        $('#' + uuid).find('.check_domain_whois_status_area').empty();
        var render_status = render_status_view(data.parse);
        $('#' + uuid).find('.check_domain_whois_status_area').append(render_status);
    }
}

function identify_domain(domain)
{
    var result = {
        extension: '',
        ascii_domain: '',
        rdap_url: ''
    };
    var rdap_data = JSON.parse(get_rdap_data());
    var rdap_data_extend = JSON.parse(get_rdap_data_extend());
    rdap_data = {...rdap_data, ...rdap_data_extend};
    var parse_domain = domain.replace(/\s+/g, '');
    if(parse_domain.length == 0)
    {
        return result;
    }

    if(typeof(parse_domain) === 'string')
    {
        if(!isAsciiString(parse_domain))
        {
            parse_domain = punycode.toASCII(parse_domain);
        }
        result.ascii_domain = parse_domain;

        let spl_domain = parse_domain.split('.');
        if(spl_domain.length > 0)
        {
            result.extension = spl_domain.at(-1);
            // pseudo sld
            if(spl_domain.length > 2)
            {
                if((spl_domain.at(-1) === 'com' && ['br', 'cn', 'de', 'eu', 'gr', 'ru',
                                                    'sa', 'uk', 'us', 'za', 'jpn'].includes(spl_domain.at(-2)))
                    || (spl_domain.at(-1) === 'net' && ['gb', 'in', 'se', 'uk'].includes(spl_domain.at(-2)))
                )
                {
                    result.extension = spl_domain.at(-2) + '.' + spl_domain.at(-1);
                }
                else if(spl_domain.at(-1) === 'uz' && ['com', 'co', 'net', 'org'].includes(spl_domain.at(-2)))
                {
                    result.extension = '';
                }
            }
        }
    }

    if(result.extension in rdap_data)
    {
        if(['de', 've', 'tz', 'uz', 'kg', "ml", "si", "ye", "ch", "li"].includes(result.extension))
        {
            // Bypass: Response body is not available to scripts (Reason: CORS Missing Allow Origin)
            result.rdap_url = '/api/v1/proxy/rdap?domain=' + parse_domain;
        }
        else
        {
            result.rdap_url = rdap_data[result.extension].rdap + "domain/" + parse_domain;
        }
    }
    return result;
}

function query_whois_data(domain, uuid, is_rdap)
{
    $.ajax({
        type: "POST",
        url: "/api/v1/whois",
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        crossDomain: false,
        data: JSON.stringify ({"domain": domain}),

        success:  function (data){
            $('#' + uuid).find('.check_domain_whois_data_area').empty();
            if(data.status)
            {
                $('#' + uuid).find('.check_domain_whois_data_area').append(data.result);
            }
            $('#' + uuid).find('.check_domain_whois_data_no_progress').removeClass('d-none');
            $('#' + uuid).find('.check_domain_whois_data_progress').addClass('d-none');
            // Some RDAP data does not contain full data. We can use WHOIS to fill it.
            if('parse' in data && data.parse)
            {
                re_render_view(data, uuid, is_rdap);
            }
        },
        error: function (err){
        },
        complete: function (data) {
        }
    });
}

function isAsciiString(text)
{
    return /^[\x00-\x7F]+$/g.test(text);
} 

async function query_rdap_data(domain_url)
{
    return $.ajax({
        type: "GET",
        url: domain_url,
        success:  function (data){
            
        },
        error: function (err){
            
        },
        complete: function (data) {
        },
        timeout: 5000,
    });
}

async function query_single_rdap_domain(domain, index, total_domain, type)
{
    let parse_domain = identify_domain(domain);
    var result = rdap_custom_data();
    var is_rdap = false;

    if(parse_domain.rdap_url)
    {
        is_rdap = true;
        try {
            result = await query_rdap_data(parse_domain.rdap_url);
        } catch (error) {
            console.log('Error!: ', error);
        }
    }

    let uuid = crypto.randomUUID();
    var parse_rdap = result = rdap_parse_data(result);
    var rdap_render = rdap_render_view(parse_domain.ascii_domain, parse_rdap, uuid);
    $(rdap_render).insertAfter('#check_domain_search');
    //
    query_whois_data(parse_domain.ascii_domain, uuid, is_rdap);
    
    if((index + 1) >= total_domain)
    {
        if(type === 'multi')
        {
            $('#multi_domain_area_input').removeClass('d-none');
            $('#multi_domain_area_btn').removeClass('d-none');
        }
        else
        {
            $('#single_domain_area').removeClass('d-none');
        }
        $('#check_domain_progress').addClass('d-none');
    }
    
}

// Event

var timeout_value = 1000;

remove_hide_btn_view($('input[name="radio_inline_multi_domain"]:checked').attr('value'));

$('input[name="radio_inline_multi_domain"][value="single"], input[name="radio_inline_multi_domain"][value="multi"]').change(function() {
    let query_radio = '';
    if($(this).attr('value') === 'multi')
    {
        query_radio = 'input[name="radio_inline_multi_domain"][value="single"]';
    }
    else
    {
        query_radio = 'input[name="radio_inline_multi_domain"][value="multi"]';
    }
    remove_hide_btn_view($(this).attr('value'));
    $(query_radio).removeAttr("checked");
    $(this).attr('checked', true);
});

$(document).on('click', '#single_domain_btn', function(){
    $('.check_domain_result_area').remove();
    var domain = $('#single_domain_input').val();

    $('#single_domain_area').addClass('d-none');
    $('#check_domain_progress').removeClass('d-none');

    setTimeout(function(){ query_single_rdap_domain(domain, 0, 1, 'single'); }, timeout_value);
});

$('#single_domain_input').keydown(function(event){    
    if (event.which == 13) {
        $('#single_domain_btn').trigger('click');
    }
    $('.sheetjs_export_excel').removeClass('d-none');
});

$(document).on('click', '#multi_domain_btn', function(){
    $('.check_domain_result_area').remove();
    var arr_domain = $('#multi_domain_input').val().split(/\r?\n/);

    $('#multi_domain_area_input').addClass('d-none');
    $('#multi_domain_area_btn').addClass('d-none');
    $('#check_domain_progress').removeClass('d-none');

    var total_domain = arr_domain.length;
    arr_domain.forEach(function(domain, index)
    {
        setTimeout(function(){ query_single_rdap_domain(domain, index, total_domain, 'multi'); }, index * timeout_value);
    });
    $('.sheetjs_export_excel').removeClass('d-none');
});

$(window).scroll(function() {
    if ($(window).scrollTop() > 300) {
        $('.btn-scroll-top').addClass('show');
    } else {
        $('.btn-scroll-top').removeClass('show');
    }
});

$('.btn-scroll-top').on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop:0}, '300');
});

new ClipboardJS('.btn_check_domain_clipboard', {
    text: function(trigger) {
        var result = $(trigger.parentElement.outerHTML).find('input').attr('value');
        $.toast({
            text: '<div style="color: white;">' + result + '</div>', // Text that is to be shown in the toast
            heading: 'Copied!', // Optional heading to be shown on the toast
            icon: 'warning', // Type of toast icon
            showHideTransition: 'fade', // fade, slide or plain
            allowToastClose: true, // Boolean value true or false
            hideAfter: 3000, // false to make it sticky or number representing the miliseconds as time after which toast needs to be hidden
            stack: 5, // false if there should be only one toast at a time or a number representing the maximum number of toasts to be shown at a time
            position: 'top-center', // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values
            bgColor: '#4299e1',
            textColor: 'white',
            
            textAlign: 'left',  // Text alignment i.e. left, right or center
            loader: true,  // Whether to show loader or not. True by default
            loaderBg: '#2fb344',  // Background color of the toast loader
            beforeShow: function () {}, // will be triggered before the toast is shown
            afterShown: function () {}, // will be triggered after the toat has been shown
            beforeHide: function () {}, // will be triggered before the toast gets hidden
            afterHidden: function () {}  // will be triggered after the toast has been hidden
        });
        return result;
    }
});

$(document).on('click', '.sheetjs_export_excel', function(){
    var data = [];
    
    var domain_area = $('.check_domain_result_area');
    for(const area_item of domain_area.toArray()){
        var label_domain = $(area_item).find('#label_domain').text();
        var registrar = $(area_item).find('#input_registrar').attr('value');
        var registrar_url = $(area_item).find('#input_registrar_url').attr('value');
        var creation_date = $(area_item).find('#input_creation_date').attr('value');
        var updated_date = $(area_item).find('#input_updated_date').attr('value');
        var expiry_date = $(area_item).find('#input_expiry_date').attr('value');

        var arr_status = [];
        var status_obj = $(area_item).find('.check_domain_whois_status_area > input');
        
        for(const item_status of status_obj.toArray()) {
            var raw_status = $(item_status).attr('value');
            if(raw_status !== undefined && raw_status.length > 0){
                arr_status.push(raw_status);
            }
        }
        data.push([label_domain, registrar, registrar_url, creation_date, updated_date, expiry_date, arr_status.join('\r\n')]);
    }

    // Create workbook & add worksheet
    var workbook = new ExcelJS.Workbook();
    var worksheet = workbook.addWorksheet('Domains');

    // add column headers
    worksheet.columns = [
        { header: 'Domain Name', width: 20},
        { header: 'Registrar', width: 20},
        { header: 'Registrar URL', width: 50},
        { header: 'Creation Date', width: 30},
        { header: 'Updated Date', width: 30},
        { header: 'Expiry Date', width: 30},
        { header: 'Status', width: 50}
    ];

    for(const item of data){
        // Add rows as Array values
        worksheet.addRow(item);
    }

    // Set Style
    const font_size = 12;
    const font = { name: 'Arial', size: font_size };
    const header_alignment = { vertical: 'middle', horizontal: 'center' };
    const normal_alignment = { vertical: 'middle', horizontal: 'left' };

    var line_length = data.length;
    line_length += 1; // Header

    for(let i=1; i <= line_length; i++){
        if(i === 1)
        {
            var header_font = {...font};
            header_font.bold = true;
            worksheet.getRow(i).font = header_font;
            worksheet.getRow(i).alignment = header_alignment;
        }
        else
        {
            worksheet.getRow(i).font = font;
            worksheet.getRow(i).alignment = normal_alignment;

            var wrap_text = { ...normal_alignment };
            wrap_text.wrapText = true;

            if(worksheet.getRow(i).model.cells.length > 6)
            {
                // Status Cell
                var status_cell = worksheet.getRow(i).model.cells[6].address;
                worksheet.getCell(status_cell).alignment = wrap_text;
                try {
                    var status_height = Math.ceil((worksheet.getCell(status_cell).text.split('\r\n')).length * (font_size + 4));
                    worksheet.getRow(i).height = status_height;
                } catch (error) {
                    
                }
            }
        }
    }

    // Save workbook to disk
    try {
        workbook.xlsx.writeBuffer().then((buffer) => {
            const blob = new Blob([buffer], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
            saveAs(blob, 'data.xlsx');
        });
    } catch (error) {
        console.log('Error in excel');
    }
    
});

$(document).on('click', '#generate_domain_keyword_cc_sld', function(){
    var data = [];
    var dict_cc = {
        "cctld_ac": "ac",
        "cctld_ad": "ad",
        "cctld_ae": "ae",
        "cctld_af": "af",
        "cctld_ag": "ag",
        "cctld_ai": "ai",
        // "cctld_al": "al",
        "cctld_am": "am",
        // "cctld_ao": "ao",
        // "cctld_aq": "aq",
        "cctld_ar": "ar",
        "cctld_as": "as",
        "cctld_at": "at",
        "cctld_au": "au",
        "cctld_aw": "aw",
        "cctld_ax": "ax",
        // "cctld_az": "az",
        // "cctld_ba": "ba",
        "cctld_bb": "bb",
        "cctld_bd": "bd",
        "cctld_be": "be",
        "cctld_bf": "bf",
        "cctld_bg": "bg",
        "cctld_bh": "bh",
        "cctld_bi": "bi",
        "cctld_bj": "bj",
        // "cctld_bl": "bl",
        "cctld_bm": "bm",
        "cctld_bn": "bn",
        "cctld_bo": "bo",
        // "cctld_bq": "bq",
        "cctld_br": "br",
        "cctld_bs": "bs",
        "cctld_bt": "bt",
        // "cctld_bv": "bv",
        "cctld_bw": "bw",
        "cctld_by": "by",
        "cctld_bz": "bz",
        "cctld_ca": "ca",
        "cctld_cc": "cc",
        "cctld_cd": "cd",
        "cctld_cf": "cf",
        "cctld_cg": "cg",
        "cctld_ch": "ch",
        "cctld_ci": "ci",
        "cctld_ck": "ck",
        "cctld_cl": "cl",
        "cctld_cm": "cm",
        "cctld_cn": "cn",
        "cctld_co": "co",
        "cctld_cr": "cr",
        "cctld_cu": "cu",
        "cctld_cv": "cv",
        "cctld_cw": "cw",
        "cctld_cx": "cx",
        "cctld_cy": "cy",
        "cctld_cz": "cz",
        "cctld_de": "de",
        "cctld_dj": "dj",
        "cctld_dk": "dk",
        "cctld_dm": "dm",
        "cctld_do": "do",
        "cctld_dz": "dz",
        "cctld_ec": "ec",
        "cctld_ee": "ee",
        "cctld_eg": "eg",
        "cctld_eh": "eh",
        "cctld_er": "er",
        "cctld_es": "es",
        "cctld_et": "et",
        "cctld_eu": "eu",
        "cctld_fi": "fi",
        "cctld_fj": "fj",
        "cctld_fk": "fk",
        "cctld_fm": "fm",
        "cctld_fo": "fo",
        "cctld_fr": "fr",
        "cctld_ga": "ga",
        // "cctld_gb": "gb",
        "cctld_gd": "gd",
        "cctld_ge": "ge",
        "cctld_gf": "gf",
        "cctld_gg": "gg",
        "cctld_gh": "gh",
        "cctld_gi": "gi",
        "cctld_gl": "gl",
        "cctld_gm": "gm",
        "cctld_gn": "gn",
        "cctld_gp": "gp",
        "cctld_gq": "gq",
        "cctld_gr": "gr",
        "cctld_gs": "gs",
        "cctld_gt": "gt",
        // "cctld_gu": "gu",
        "cctld_gw": "gw",
        "cctld_gy": "gy",
        "cctld_hk": "hk",
        "cctld_hm": "hm",
        "cctld_hn": "hn",
        "cctld_hr": "hr",
        "cctld_ht": "ht",
        "cctld_hu": "hu",
        "cctld_id": "id",
        "cctld_ie": "ie",
        "cctld_il": "il",
        "cctld_im": "im",
        "cctld_in": "in",
        "cctld_io": "io",
        "cctld_iq": "iq",
        "cctld_ir": "ir",
        "cctld_is": "is",
        "cctld_it": "it",
        "cctld_je": "je",
        "cctld_jm": "jm",
        "cctld_jo": "jo",
        "cctld_jp": "jp",
        "cctld_ke": "ke",
        "cctld_kg": "kg",
        // "cctld_kh": "kh",
        "cctld_ki": "ki",
        // "cctld_km": "km",
        "cctld_kn": "kn",
        // "cctld_kp": "kp",
        "cctld_kr": "kr",
        "cctld_kw": "kw",
        "cctld_ky": "ky",
        "cctld_kz": "kz",
        "cctld_la": "la",
        "cctld_lb": "lb",
        "cctld_lc": "lc",
        "cctld_li": "li",
        "cctld_lk": "lk",
        "cctld_lr": "lr",
        "cctld_ls": "ls",
        "cctld_lt": "lt",
        "cctld_lu": "lu",
        "cctld_lv": "lv",
        "cctld_ly": "ly",
        "cctld_ma": "ma",
        "cctld_mc": "mc",
        "cctld_md": "md",
        "cctld_me": "me",
        "cctld_mf": "mf",
        "cctld_mg": "mg",
        // "cctld_mh": "mh",
        "cctld_mk": "mk",
        "cctld_ml": "ml",
        "cctld_mm": "mm",
        "cctld_mn": "mn",
        "cctld_mo": "mo",
        "cctld_mp": "mp",
        "cctld_mq": "mq",
        "cctld_mr": "mr",
        "cctld_ms": "ms",
        "cctld_mt": "mt",
        "cctld_mu": "mu",
        "cctld_mv": "mv",
        "cctld_mw": "mw",
        "cctld_mx": "mx",
        "cctld_my": "my",
        "cctld_mz": "mz",
        "cctld_na": "na",
        "cctld_nc": "nc",
        "cctld_ne": "ne",
        "cctld_nf": "nf",
        "cctld_ng": "ng",
        "cctld_ni": "ni",
        "cctld_nl": "nl",
        "cctld_no": "no",
        "cctld_np": "np",
        "cctld_nr": "nr",
        "cctld_nu": "nu",
        "cctld_nz": "nz",
        "cctld_om": "om",
        "cctld_pa": "pa",
        "cctld_pe": "pe",
        "cctld_pf": "pf",
        // "cctld_pg": "pg",
        "cctld_ph": "ph",
        "cctld_pk": "pk",
        "cctld_pl": "pl",
        "cctld_pm": "pm",
        "cctld_pn": "pn",
        "cctld_pr": "pr",
        "cctld_ps": "ps",
        "cctld_pt": "pt",
        "cctld_pw": "pw",
        // "cctld_py": "py",
        "cctld_qa": "qa",
        "cctld_re": "re",
        "cctld_ro": "ro",
        "cctld_rs": "rs",
        "cctld_ru": "ru",
        "cctld_rw": "rw",
        "cctld_sa": "sa",
        "cctld_sb": "sb",
        "cctld_sc": "sc",
        "cctld_sd": "sd",
        "cctld_se": "se",
        "cctld_sg": "sg",
        "cctld_sh": "sh",
        "cctld_si": "si",
        // "cctld_sj": "sj",
        "cctld_sk": "sk",
        "cctld_sl": "sl",
        "cctld_sm": "sm",
        "cctld_sn": "sn",
        "cctld_so": "so",
        // "cctld_sr": "sr",
        "cctld_ss": "ss",
        "cctld_st": "st",
        "cctld_su": "su",
        "cctld_sv": "sv",
        "cctld_sx": "sx",
        "cctld_sy": "sy",
        "cctld_sz": "sz",
        "cctld_tc": "tc",
        "cctld_td": "td",
        "cctld_tf": "tf",
        "cctld_tg": "tg",
        "cctld_th": "th",
        "cctld_tj": "tj",
        "cctld_tk": "tk",
        "cctld_tl": "tl",
        "cctld_tm": "tm",
        "cctld_tn": "tn",
        "cctld_to": "to",
        "cctld_tr": "tr",
        "cctld_tt": "tt",
        "cctld_tv": "tv",
        "cctld_tw": "tw",
        "cctld_tz": "tz",
        "cctld_ua": "ua",
        "cctld_ug": "ug",
        "cctld_uk": "uk",
        // "cctld_um": "um",
        "cctld_us": "us",
        "cctld_uy": "uy",
        "cctld_uz": "uz",
        "cctld_va": "va",
        "cctld_vc": "vc",
        "cctld_ve": "ve",
        "cctld_vg": "vg",
        "cctld_vi": "vi",
        "cctld_vn": "vn",
        "cctld_vu": "vu",
        "cctld_wf": "wf",
        "cctld_ws": "ws",
        "cctld_ye": "ye",
        "cctld_yt": "yt",
        "cctld_za": "za",
        "cctld_zm": "zm",
        "cctld_zw": "zw"
    };
    var keyword = $("#generate_domain_keyword_input").val();
    if(keyword === undefined)
    {
        keyword = '';
    }
    for(var key in dict_cc)
    {
        data.push(keyword + '.' + dict_cc[key]);
    }

    if(data.length > 0)
    {
        $('#generate_domain_keyword_result').val(''); // Remove old values
        $('#generate_domain_keyword_result').val(data.join('\n'));
    }
});

new ClipboardJS('#generate_domain_cut_cc_sld', {
    text: function(trigger) {
        var result = $('#generate_domain_keyword_result').val();
        $.toast({
            text: '<div style="color: white;">Data was copied!</div>',
            heading: 'Copied!',
            icon: 'warning',
            showHideTransition: 'fade',
            allowToastClose: true,
            hideAfter: 3000,
            stack: 5,
            position: 'top-center',
            bgColor: '#4299e1',
            textColor: 'white',
            textAlign: 'left',
            loader: true,
            loaderBg: '#2fb344',
        });
        // Remove data
        $('#generate_domain_keyword_result').val('');
        $('#generate_domain_keyword_input').val('');
        return result;
    }
});