define(function () {
    var vm = function () {
        var self = this;

        // Observables
        self.slug = ko.observable('');

        // Functions
        self.canActivate = function () {
            return true;
        };

        self.activate = function () {
            // Set the initial value of the slug
            debugger;
            self.slug($('#slug').val());

            // Attach to changes of the title
            $('#name').keyup(function(){
                var title = $.trim($(this).val()).replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '-').toLowerCase();
                self.slug(title);
                $('#slug').val(title);
            });
        };

        return self;
    };

    return vm;
});