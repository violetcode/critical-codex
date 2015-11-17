/*!
 * UnderTasker
 * Copyright 2014 Tyler Rilling, some parts loosely based off of Bootstrap
 * Licensed under MIT (https://github.com/underlost/Undertasker/blob/master/LICENSE)
 */

module.exports = function (grunt) {
  'use strict';

  // Force use of Unix newlines
  grunt.util.linefeed = '\n';

  RegExp.quote = function (string) {
    return string.replace(/[-\\^$*+?.()|[\]{}]/g, '\\$&');
  };

  var fs = require('fs');
  var path = require('path');

  // Project configuration.
  grunt.initConfig({

    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*!\n' +
            ' * <%= pkg.name %> v<%= pkg.version %> (Built with UnderTasker)\n' +
            ' */\n',
    jqueryCheck: 'if (typeof jQuery === \'undefined\') { throw new Error(\'UnderTasker\\\'s JavaScript requires jQuery\') }\n\n',

    // Task configuration.
    clean: {
      dist: ['dist']
    },

    coffee: {
      compile: {
        files: {
          'd20/static/js/app.js': 'static_assets/coffee/app.coffee', // 1:1 compile
          // 'd20/static/js/app.js': ['static_assets/coffee/*.coffee'] // compile and concat into single file
        }
      },
    },

    jshint: {
      options: {
        jshintrc: 'static_assets/js/.jshintrc'
      },
      grunt: {
        options: {
          jshintrc: 'grunt/.jshintrc'
        },
        src: ['Gruntfile.js', 'grunt/*.js']
      },
      src: {
        src: 'static_assets/js/*.js'
      },
      test: {
        src: 'static_assets/js/tests/unit/*.js'
      }
    },

    jscs: {
      options: {
        config: 'static_assets/js/.jscsrc'
      },
      grunt: {
        options: {
          requireCamelCaseOrUpperCaseIdentifiers: null,
          requireParenthesesAroundIIFE: true
        },
        src: '<%= jshint.grunt.src %>'
      },
      src: {
        src: '<%= jshint.src.src %>'
      },
      test: {
        src: '<%= jshint.test.src %>'
      },
      assets: {
        src: '<%= jshint.assets.src %>'
      }
    },

    concat: {
      options: {
        banner: '<%= banner %>\n<%= jqueryCheck %>',
        stripBanners: false
      },
      undertask: {
        src: [
          'static_assets/js/transition.js',
          'static_assets/js/alert.js',
          'static_assets/js/button.js',
          'static_assets/js/carousel.js',
          'static_assets/js/collapse.js',
          'static_assets/js/dropdown.js',
          'static_assets/js/modal.js',
          'static_assets/js/tooltip.js',
          'static_assets/js/popover.js',
          'static_assets/js/scrollspy.js',
          'static_assets/js/tab.js',
          'static_assets/js/affix.js',
          'static_assets/js/typeahead.bundle.js',
          'static_assets/js/jquery.autosize.min.js',
          'static_assets/js/jquery.history.min.js',
          'static_assets/js/handler.js'
          ],
        dest: 'dist/js/<%= pkg.slug %>.js'
      }
    },

    uglify: {
      options: {
        report: 'min'
      },
      undertask: {
        options: {
          banner: '<%= banner %>'
        },
        src: '<%= concat.undertask.dest %>',
        dest: 'dist/js/<%= pkg.slug %>.min.js'
      }
    },

    qunit: {
      options: {
        inject: 'static_assets/js/tests/unit/phantom.js'
      },
      files: 'static_assets/js/tests/index.html'
    },

    less: {
      compileCore: {
        options: {
          strictMath: true,
          sourceMap: true,
          outputSourceFiles: true,
          sourceMapURL: '<%= pkg.slug %>.css.map',
          sourceMapFilename: 'dist/css/<%= pkg.slug %>.css.map'
        },
        files: {
          'dist/css/<%= pkg.slug %>.css': 'static_assets/less/<%= pkg.slug %>.less'
        }
      },
      minify: {
        options: {
          cleancss: true,
          report: 'min'
        },
        files: {
          'dist/css/<%= pkg.slug %>.min.css': 'dist/css/<%= pkg.slug %>.css'
        }
      }
    },

    autoprefixer: {
      options: {
        browsers: ['last 2 versions', 'ie 8', 'ie 9', 'android 2.3', 'android 4', 'opera 12']
      },
      core: {
        options: {
          map: true
        },
        src: 'dist/css/<%= pkg.slug %>.css'
      }
    },

    csslint: {
      options: {
        csslintrc: 'static_assets/less/.csslintrc'
      },
      src: [
        'dist/css/<%= pkg.slug %>.css'
      ]
    },

    cssmin: {
      options: {
        keepSpecialComments: '*',
        noAdvanced: true, // turn advanced optimizations off until the issue is fixed in clean-css
        report: 'min',
        compatibility: 'ie8'
      }
    },

    usebanner: {
      options: {
        position: 'top',
        banner: '<%= banner %>'
      },
      files: {
        src: 'dist/css/*.css'
      }
    },

    csscomb: {
      options: {
        config: 'static_assets/less/.csscomb.json'
      },
      dist: {
        expand: true,
        cwd: 'dist/css/',
        src: ['*.css', '!*.min.css'],
        dest: 'dist/css/'
      }
    },

    imagemin: {
      dynamic: {
        files: [{
        expand: true,
        cwd: 'static_assets/img/',
        src: ['**/*.{png,jpg,gif}'],
        dest: 'dist/img/'
      }]
      }
    },

    copy: {
      fonts: {
        expand: true,
        cwd: './src',
        src: [
          'fonts/*'
        ],
        dest: 'dist'
      },
      static_dist: {
          expand: true,
          cwd: './dist',
          src: [
          '{css,js}/*.min.*',
          'css/*.map',
          'fonts/*',
          'img/*'
          ],
          dest: 'static_assets/site/static'
      },
      dist: {
        expand: true,
        cwd: './dist',
        src: [
          '{css,js}/*.min.*',
          'css/*.map',
          'fonts/*',
          'img/*'
        ],
        dest: 'd20/static'
      },
    },

    connect: {
      server: {
        options: {
          port: 3000,
          base: '.'
        }
      }
    },

    jekyll: {
      options : {
        bundleExec: true,
        src : 'static_assets/site',
      },
      site: {}
    },

    validation: {
      options: {
        charset: 'utf-8',
        doctype: 'HTML5',
        failHard: true,
        reset: true,
        relaxerror: [
          'Bad value X-UA-Compatible for attribute http-equiv on element meta.',
          'Element img is missing required attribute src.'
        ]
      },
      files: {
        src: '_gh_pages/**/*.html'
      }
    },

    watch: {
      src: {
        files: '<%= jshint.src.src %>',
        tasks: ['jshint:src', 'qunit']
      },
      test: {
        files: '<%= jshint.test.src %>',
        tasks: ['jshint:test', 'qunit']
      },
      less: {
        files: 'static_assets/less/*.less',
        tasks: 'less'
      }
    },

    git_deploy: {
      github: {
        options: {
          url: 'git@github.com:underlost/d20.git',
          branch: 'gh-pages',
          message: 'Deployed with grunt' // Commit message
        },
        src: '_gh_pages'
      },
    }

  });

  // These plugins provide necessary tasks.
  require('load-grunt-tasks')(grunt, {scope: 'dependencies'});
  require('time-grunt')(grunt);

  // Coffee build task.
  grunt.registerTask('build-coffee', ['coffee']);

  // JS distribution task.
  grunt.registerTask('build-js', ['concat', 'uglify']);

  // IMG distribution task.
  grunt.registerTask('build-img', ['imagemin']);

  // CSS build task.
  grunt.registerTask('less-compile', ['less:compileCore']);
  grunt.registerTask('build-css', ['less-compile', 'autoprefixer', 'usebanner', 'csscomb', 'less:minify', 'cssmin']);

  // HTML build/validation site task
  grunt.registerTask('build-site', ['jekyll', 'validation']);

  // Git Deploy task
  grunt.registerTask('git-deploy', ['git_deploy:github']);

  // Test task.
  grunt.registerTask('test', ['build-css', 'csslint', 'jshint', 'jscs', 'qunit']);

  // Build static assets and HTML
  grunt.registerTask('build', ['clean', 'build-coffee', 'build-css', 'build-js', 'build-img', 'build-site', 'copy:fonts', 'copy:dist']);

  // Only build static assets, not html
  grunt.registerTask('dist', ['clean', 'build-coffee', 'build-css', 'build-js', 'build-img', 'copy:fonts', 'copy:dist', 'copy:static_dist']);

  // Full Deploy
  grunt.registerTask('deploy', ['git-deploy']);

};
