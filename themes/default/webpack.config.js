const fs = require("fs");
const path = require("path");
const glob = require("glob");

const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");

const templatePath =  path.join("source", "templates");

function getContext(jsonfile) {
  /*
  / Returns context object
  */
  try {
    file_path = path.join(__dirname, "source", "data", jsonfile);
    var context = JSON.parse(fs.readFileSync(file_path, "utf8"));
    return context;
  } catch {
    return {};
  }
}

function toPlugin(fileName) {
  var file = fileName.replace(`${templatePath}/`, "");
  var chunk_name = file.replace(/\.njk$/, "");
  var jsonfile = file.replace(/\.njk$/, ".json");
  return new HtmlWebpackPlugin({
    inject: false,
    chunks: ["main", "shared", "runtime", chunk_name],
    template: fileName,
    filename: file.replace(/\.njk$/, ".html"),
    templateParameters: getContext(jsonfile),
  });
}

function getTemplates() {
  var templates = glob.sync(`${templatePath}/!(_*).njk`);
  return templates.map(toPlugin);
}

const NunjucksHTMLPlugins = getTemplates();

module.exports = {
  target: ["web", "es5"],
  context: __dirname,
  mode: "development",
  entry: {
    index: {
      import: "./source/js/index.js",
      dependOn: "shared",
    },
    account: {
      import: "./source/js/account.js",
      dependOn: "shared",
    },
    main: {
      import: "./source/js/main.js",
      dependOn: "shared",
    },
    shared: [
      "bootstrap/dist/js/bootstrap.bundle.js",
      "regenerator-runtime/runtime.js",
      "alpinejs",
    ],
  },
  output: {
    path: path.resolve("./static/theme_default/"),
    // chunkFilename: "js/[name].bundle.js",
    filename: "js/[name].bundle.js",
    clean: true,
  },
  optimization: {
    runtimeChunk: "single",
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          format: {
            comments: false,
          },
        },
        extractComments: false,
      }),
      new CssMinimizerPlugin({
        minimizerOptions: {
          preset: [
            "default",
            {
              discardComments: { removeAll: true },
            },
          ],
        },
      }),
    ],
  },
  devServer: {
    host: "127.0.0.1",
    port: 9000,
    hot: true,
    allowedHosts: "all",
    static: {
      directory: path.join(__dirname, "dist"),
      watch: true,
    },
    devMiddleware: {
      writeToDisk: true,
    },
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
      {
        test: /\.js$/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [
              [
                "@babel/preset-env",
                {
                  targets: {
                    esmodules: true,
                  },
                },
              ],
            ],
          },
        },
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // fallback to style-loader in development
          MiniCssExtractPlugin.loader,
          "css-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.(eot|woff|woff2|ttf)$/,
        type: "asset/resource",
        generator: {
          filename: "fonts/[name][ext]",
        },
      },
      {
        test: /\.njk$/,
        use: [
          {
            loader: "simple-nunjucks-loader",
            options: {
              assetsPaths: ["./source"],
              searchPaths: [`./${templatePath}`],
            },
          },
        ],
      },
      {
        test: /\.(svg|png|jpe?g|gif|ico)$/i,
        type: "asset/resource",
        generator: {
          filename: "img/[name][ext]",
        },
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      inject: false,
      chunks: ["main", "shared", "runtime", "index"],
      template: `${templatePath}/index.njk`,
      filename: "index.html",
      templateParameters: getContext("index.json"),
    }),
    new HtmlWebpackPlugin({
      inject: false,
      chunks: ["main", "shared", "runtime", "projects"],
      template: `${templatePath}/projects.njk`,
      filename: "projects.html",
      templateParameters: getContext("projects.json"),
    }),
    new HtmlWebpackPlugin({
      inject: false,
      chunks: ["main", "shared", "runtime", "projects"],
      template: `${templatePath}/courses.njk`,
      filename: "courses.html",
      templateParameters: getContext("projects.json"),
    }),
    new HtmlWebpackPlugin({
      inject: false,
      chunks: ["main", "shared", "runtime", "projects"],
      template: `${templatePath}/projects_detail.njk`,
      filename: "projects_detail.html",
      templateParameters: getContext("projects_detail.json"),
    }),
    new HtmlWebpackPlugin({
      inject: false,
      chunks: ["main", "shared", "runtime", "blog"],
      template: `${templatePath}/blog.njk`,
      filename: "blog.html",
      templateParameters: getContext("blog.json"),
    }),
    new HtmlWebpackPlugin({
      inject: false,
      chunks: ["main", "shared", "runtime", "blog"],
      template: `${templatePath}/blog_detail.njk`,
      filename: "blog_detail.html",
      templateParameters: getContext("blog_detail.json"),
    }),
    new HtmlWebpackPlugin({
      inject: false,
      chunks: ["main", "shared", "runtime", "partners"],
      template: `${templatePath}/partners.njk`,
      filename: "partners.html",
      templateParameters: getContext("partners.json"),
    }),
    new CleanWebpackPlugin({
      dry: true,
    }),
    new CopyPlugin({
      patterns: [
        { from: "./source/img", to: "./img" },
        { from: "./source/css/plugins", to: "./css/plugins" },
        { from: "./source/js/plugins", to: "./js/plugins" },
      ],
    }),
    // new BundleTracker({
    //   filename: "./webpack-stats.json",
    // }),
    new MiniCssExtractPlugin({
      filename: "css/[name].bundle.css",
    }),
  ],
};
