#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sysfs.h>
#include <linux/delay.h>
#include <linux/platform_device.h>
#include <linux/err.h>
#include <linux/device.h>
#include <linux/interrupt.h>
#include <linux/irq.h>
#include <linux/of_gpio.h>
#include <asm/uaccess.h>
#include <linux/kdev_t.h>
#include <linux/slab.h>
#include <linux/workqueue.h>

struct qca4020_data {
    struct platform_device *pdev;
    int flag;
    int gpio_int;
    int irq;
};

static struct qca4020_data* data;

static irqreturn_t qca4020_interrupt_handler(int irq, void *ptr)
{
    data->flag = 1;

    return IRQ_HANDLED;
}

static ssize_t qca4020_value_store(struct device *dev, struct device_attribute* attr,
                                            const char *buf, size_t len)
{
    data->flag = 0;
    
    return len;
}

static ssize_t qca4020_value_show(struct device *dev, struct device_attribute* attr,
                                            char *buf)
{
    ssize_t ret = sprintf(buf, "%d\n", data->flag);
                
    return ret;
}


static DEVICE_ATTR(value, 0664, qca4020_value_show, qca4020_value_store);

static int QCA4020_probe(struct platform_device *pdev)
{
    int result;
    struct device_node* node = pdev->dev.of_node;

    printk("qca4020 probe enter\n");
    data = devm_kzalloc(&pdev->dev, sizeof(struct qca4020_data), GFP_KERNEL);
    if (!data) {
        pr_err("%s kzalloc error\n", __FUNCTION__);
        return -ENOMEM;
    }

    dev_set_drvdata(&pdev->dev, data);

    data->gpio_int = of_get_named_gpio(node, "gpio_int", 0);
    if (!gpio_is_valid(data->gpio_int)) {
        pr_err("gpio_int not specified\n");
        goto err;
    } else {
        result = gpio_request(data->gpio_int, "qca_gpio");
        if (result < 0) {
            pr_err("Unable to request qca_gpio\n");
            goto err;
        } else {
            gpio_direction_input(data->gpio_int);
        }
    }

    data->irq = gpio_to_irq(data->gpio_int);
    result = request_irq(data->irq, qca4020_interrupt_handler,
                                                 IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING, "qca4020_intr", data);
    if (result < 0) {
        pr_err("Unable to request irq\n");
        goto err;
    }

    result = sysfs_create_file(&pdev->dev.kobj, &dev_attr_value.attr);
    if (result < 0) {
        printk("sysfs create file failed\n");
        goto err;
    }

    printk(KERN_INFO "QCA4020 probe success\n");

    return 0;

err:
    kfree(data);
    printk(KERN_ERR "QCA4020 probe failed\n");
    return -EINVAL;
}

static int QCA4020_remove(struct platform_device *pdev)
{
        gpio_free(data->gpio_int);
        kfree(data);
                
        return 0;
}

static struct of_device_id mach_match_table[] = {
    { .compatible = "linux,qca4020"},
    { },
};

static struct platform_driver QCA4020_driver = {
    .probe = QCA4020_probe,
    .remove = QCA4020_remove,
    .driver = {
        .owner = THIS_MODULE,
        .name = "QCA4020GPIO",
        .of_match_table = mach_match_table,
    },
};

module_platform_driver(QCA4020_driver);
MODULE_AUTHOR("yanggh0703@thundersoft.com");
MODULE_LICENSE("GPL");
