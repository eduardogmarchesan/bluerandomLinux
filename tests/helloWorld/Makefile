obj-m += hello_world.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules || echo "Erro na compilação do módulo."

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

load:
	sudo insmod hello_world.ko

unload:
	sudo rmmod hello_world

dmesg:
	dmesg | tail -n 20
