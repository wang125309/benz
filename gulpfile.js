var gulp = require('gulp');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var jade = require('gulp-jade');
var css_minify = require('gulp-minify-css');
var browserify = require('gulp-browserify');

gulp.task('lint',function(){
    gulp.src('./assets/js-modify/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
    });

gulp.task('sass-portal-lib',function(){
    gulp.src('./assets/css-modify/portal/lib/*.sass')
        .pipe(sass())
        .pipe(css_minify())
        .pipe(gulp.dest('./assets/css/portal/lib/'));
    });

gulp.task('sass-portal',function(){
    gulp.src('./assets/css-modify/portal/*.sass')
        .pipe(sass())
        .pipe(css_minify())
        .pipe(gulp.dest('./assets/css/portal/'));
    });

gulp.task('sass-spot-lib',function(){
    gulp.src('./assets/css-modify/spot/lib/*.sass')
        .pipe(sass())
        .pipe(css_minify())
        .pipe(gulp.dest('./assets/css/spot/lib/'));
    });

gulp.task('sass-spot',function(){
    gulp.src('./assets/css-modify/spot/*.sass')
        .pipe(sass())
        .pipe(css_minify())
        .pipe(gulp.dest('./assets/css/spot/'));
    });

gulp.task('sass-back',function(){
    gulp.src('./assets/css-modify/backend/*.sass')
        .pipe(sass())
        .pipe(css_minify())
        .pipe(gulp.dest('./assets/css/backend/'));
});
gulp.task('sass-back-lib',function(){
    gulp.src('./assets/css-modify/backend/lib/*.sass')
        .pipe(sass())
        .pipe(css_minify())
        .pipe(gulp.dest('./assets/css/backend/lib/'));
});
gulp.task('sass',function(){
    gulp.src('./assets/css-modify/*.sass')
        .pipe(sass())
        .pipe(css_minify())
        .pipe(gulp.dest('./assets/css'));
});

var js_files_backend = ['backend/login','backend/index','backend/userList','backend/taskList','backend/bonus','backend/share','backend/weixin','portal/portal','portal/login','portal/taskList','spot/login'];

gulp.task('js',function(){
    for (i in js_files_backend) {
        gulp.src('./assets/js-modify/'+js_files_backend[i]+'.js')
			.pipe(browserify())
			.pipe(concat('.js'))
            .pipe(gulp.dest('./assets/js/'))
            .pipe(rename(js_files_backend[i]+'.min.js'))
            .pipe(uglify())
            .pipe(gulp.dest('./assets/js/'));
    }
});

gulp.task('jade-spot',function(){
    var jade_files = {};
    gulp.src('./templates/jade/spot/*.jade')
        .pipe(jade({
            locals:jade_files
        }))
        .pipe(gulp.dest('./templates/spot/'))
});
gulp.task('jade-spot-lib',function(){
    var jade_files = {};
    gulp.src('./templates/jade/spot/lib/*.jade')
        .pipe(jade({
            locals:jade_files
        }))
        .pipe(gulp.dest('./templates/spot/lib/'))
});
gulp.task('jade-back',function(){
    var jade_files = {};
    gulp.src('./templates/jade/backend/*.jade')
        .pipe(jade({
            locals:jade_files
        }))
        .pipe(gulp.dest('./templates/backend/'))
});
gulp.task('jade-back-lib',function(){
    var jade_files = {};
    gulp.src('./templates/jade/backend/lib/*.jade')
        .pipe(jade({
            locals:jade_files
        }))
        .pipe(gulp.dest('./templates/backend/lib/'))
});
gulp.task('jade-portal',function(){
    var jade_files = {};
    gulp.src('./templates/jade/portal/*.jade')
        .pipe(jade({
            locals:jade_files
        }))
        .pipe(gulp.dest('./templates/portal/'))
    });
gulp.task('jade-portal-lib',function(){
    var jade_files = {};
    gulp.src('./templates/jade/portal/lib/*.jade')
        .pipe(jade({
            locals:jade_files
        }))
        .pipe(gulp.dest('./templates/portal/lib/'))
    });
