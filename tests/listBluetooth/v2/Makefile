obj-m += bluetooth_test.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules || echo "Erro na compilação do módulo."

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

load:
	sudo insmod list_bt_devices.ko

unload:
	sudo rmmod list_bt_devices.c

dmesg:
	dmesg | tail -n 20
