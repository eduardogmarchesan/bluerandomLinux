#include <linux/init.h>      // Macros para funções init e exit
#include <linux/module.h>    // Necessário para todos os módulos de kernel
#include <linux/kernel.h>    // Necessário para KERN_INFO

static int __init hello_init(void) {
    printk(KERN_INFO "Hello, World!\n");
    return 0;  // Retorna 0 para indicar sucesso na carga do módulo
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye, World!\n");
}

module_init(hello_init);
module_exit(hello_exit);
