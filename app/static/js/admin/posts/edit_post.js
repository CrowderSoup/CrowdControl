define(function () {
    var vm = function () {
        var self = this;

        // Properties
        self.languages = [
            'js', 'html', 'css', 'python', 'ruby', 'php', 'c#', 'bash', 'apache', 'ini', 'nginx', 'c++', 'java', 'json',
            'sql', 'objective-c'
        ];

        self.editor = ace.edit("editor");
        self.writer = new stmd.HtmlRenderer();
        self.reader = new stmd.DocParser();

        // Observables
        self.parsed = ko.observable('');

        self.slug = ko.observable('');

        // Functions
        self.highlight = function(){
            $('#preview pre code').each(function(i, block) {
                var highlighted = hljs.highlightAuto(block.innerText);

                if(highlighted.value != null){
                    console.log(highlighted.value);
                    $(block).parent().addClass('hljs');
                    block.innerHTML = highlighted.value;
                }

                if(highlighted.language != null){
                    $(block).parent().addClass(highlighted.language);
                }
            });
        };

        self.parse = function(){
            var parsed = self.reader.parse(self.editor.getValue());
            var result = self.writer.renderBlock(parsed);

            self.parsed(result);
            $("#content").val(self.editor.getValue());

            self.highlight();
        };

        self.canActivate = function () {
            return true;
        };

        self.activate = function () {
            // Set all the options for our editor (Ace)
            setUpEditor();

            // Initial Parse on load
            self.parse();

            // Let's ensure that we have the most up-to-date content on save
            $("#page-form").submit(function(){
                $("#content").val(self.editor.getValue());
                return true;
            });

            // Set up the datetime picker
            $('.datetimepicker').datetimepicker({
                format: 'yyyy-mm-dd hh:ii:ss',
                autoclose: true,
                todayBtn: true,
                minuteStep: 15
            });

            // Set the initial value of the slug
            self.slug($('#slug').val());

            // Attach to changes of the title
            $('#title').keyup(function(){
                var title = $.trim($(this).val()).replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '-').toLowerCase();
                self.slug(title);
                $('#slug').val(title);
            });
        };

        var setUpEditor = function(){
            // Set options
            self.editor.setTheme("ace/theme/chrome");
            self.editor.getSession().setMode("ace/mode/markdown");
            self.editor.getSession().setUseWrapMode(true);

            // Set value
            self.editor.getSession().setValue($("#content").val());

            // Bind to Editor Events
            self.editor.getSession().on('change', self.parse);
            self.editor.getSession().on('blur', self.parse);
        };

        return self;
    };

    return vm;
});