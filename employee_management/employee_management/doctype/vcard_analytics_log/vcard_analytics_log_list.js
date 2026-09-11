frappe.listview_settings['VCard Analytics Log'] = {
    onload: function(listview) {
        // Clear primary action natively
        listview.page.clear_primary_action();
        
        // Aggressively hide the button in case it renders late
        setTimeout(() => {
            listview.page.clear_primary_action();
            $('.primary-action').hide();
        }, 50);
        setTimeout(() => {
            $('.primary-action').hide();
        }, 500);
    }
};