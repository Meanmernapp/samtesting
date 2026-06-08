FROM nginx:alpine
COPY index.html config.js vercel.json /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
