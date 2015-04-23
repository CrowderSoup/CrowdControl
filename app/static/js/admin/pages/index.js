define(function () {
    var vm = function () {
        var self = this;

        // Observables

        // Functions
        self.search = function(){
            window.location.href = '/admin/pages/search/' + encodeURIComponent($('#search').val());
        };

        self.canActivate = function () {
            return true;
        };

        self.activate = function () {
        };

        return self;
    };

    return vm;
});
