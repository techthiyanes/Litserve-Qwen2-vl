# QWEN2 VL
MUltimodal model
## Docker build
```docker build -t qwen2vl .```

### Docker run
```docker run -d --name qwen2vl -p 80:80 qwen2vl ```

### Descript
``` Inside of the client.py just change the base url and prediction can be made by runing: python client.py --image test.png --prompt "testing prompt"```