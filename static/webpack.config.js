const path = require('path');

module.exports = {
    entry: {
        app: './src/index.js'
    },
    watch: true,
    devtool: 'source-map',
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [{
                  loader: 'style-loader'
                }, {
                  loader: 'css-loader'
                }, {
                  loader: 'sass-loader'
                }],
            },
            {
                test: require.resolve('jquery'),
                use: [{
                loader: 'expose-loader',
                options: 'jQuery'
                },{
                loader: 'expose-loader',
                options: '$'
                }]
            }
        ]
    },
    node: {
        fs: "empty",
        child_process: 'empty'
        },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    resolve: {
        extensions: [
            '.js'
        ],
        alias: {
            'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    }
}