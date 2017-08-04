from katana.utils.migration import artifacts, deployer
# from katana import deploy, artifact
Greeter = artifacts.get("./Greeter.v.py")
greeter_address = deployer.deploy(Greeter, arguments=[5])
