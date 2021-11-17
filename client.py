import cx_Oracle
import sys

print("connecting to database.\n.\n.\n.")


def make_connection() -> cx_Oracle.connect:
    account = input('account: ')
    password = input('password: ')
    try:
        connection = cx_Oracle.connect(
            user=account.strip(),
            password=password.strip(),
            dsn="localhost:1521",
            # dsn="localhost:1521/ORCLCDB.localdomain"
        )
        print('Connect Success!\n.\n.\n.')
        return connection
    except cx_Oracle.DatabaseError:
        print("ERROR: Connection Failed!")
        return False


def print_connection_error() -> None:
    print("Check username and password")
    print("--------default user info---------")
    print("account: unist")
    print("password: unist")


def fetch_computers_order_by_name(connection: cx_Oracle.connect) -> None:
    print("\n-------------------------------------\n")
    table = [
        ['NAME', 'PRICE', 'TYPE', 'CPU', 'FEATURE'],
        ['----', '-----', '----', '---', '-----'],
    ]
    with connection.cursor() as cursor:
        for row in cursor.execute("""
            SELECT
                'A' || A_desktop.model name,
                A_DESKTOP.price price,
                'D' AS TYPE,
                A_DESKTOP.cpu cpu,
                'none' AS feature
            FROM
                DESKTOP A_desktop
            UNION
                
            SELECT
                'A' || A_LAPTOP.model name,
                A_LAPTOP.PRICE,
                'L' AS TYPE,
                A_LAPTOP.CPU,
                TO_CHAR(A_LAPTOP.WEIGHT) AS feature
            FROM
                LAPTOP A_LAPTOP
            UNION

            SELECT
                'B' || B_PC.model || B_pc.code name,
                B_pc.price,
                B_pc.TYPE,
                B_pc.cpu,
                'none' AS feature
            FROM
                PC B_pc
                
            ORDER BY name
        """):
            table.append(list(row))

    for each in table:
        print("{: >6} {: >6} {: >6} {: >6} {: >6}".format(*each))


def fetch_computers_recommended(connection: cx_Oracle.connect) -> None:
    print("\n-------------------------------------\n")
    table = [
        ['NAME', 'PRICE', 'TYPE', 'CPU', 'FEATURE'],
        ['----', '-----', '----', '---', '-----'],
    ]
    # fetch recommended computers
    with connection.cursor() as cursor:
        for row in cursor.execute("""
            SELECT
                'A' || A_desktop.model name,
                A_DESKTOP.price price,
                'D' AS TYPE,
                A_DESKTOP.cpu cpu,
                'none' AS feature
            FROM
                DESKTOP A_desktop,
                (
                SELECT
                    AVG(A_computer.price) average_price,
                    AVG(A_computer.cpu) average_cpu
                FROM
                    (
                    SELECT
                        A_DESKTOP.price price,
                        A_DESKTOP.cpu cpu
                    FROM
                        DESKTOP A_desktop
                    UNION
                    SELECT
                        A_LAPTOP.PRICE,
                        A_LAPTOP.CPU
                    FROM
                        LAPTOP A_LAPTOP				
                    ) A_computer
                ) A_computer_averages
            WHERE
                A_desktop.price < A_computer_averages.average_price
                AND A_desktop.cpu > A_computer_averages.average_cpu
            UNION
                            
            SELECT
                'A' || A_LAPTOP.model name,
                A_LAPTOP.PRICE,
                'L' AS TYPE,
                A_LAPTOP.CPU,
                TO_CHAR(A_LAPTOP.WEIGHT) AS feature
            FROM
                LAPTOP A_LAPTOP,
                (
                SELECT
                    AVG(A_computer.price) average_price,
                    AVG(A_computer.cpu) average_cpu
                FROM
                    (
                    SELECT
                        A_DESKTOP.price price,
                        A_DESKTOP.cpu cpu
                    FROM
                        DESKTOP A_desktop
                UNION
                    SELECT		
                        A_LAPTOP.PRICE,	
                        A_LAPTOP.CPU
                    FROM
                        LAPTOP A_LAPTOP	
                    ) A_computer
            ) A_computer_averages
            WHERE 
                A_LAPTOP .price < A_computer_averages.average_price
                AND A_LAPTOP .cpu > A_computer_averages.average_cpu
            UNION 

            SELECT
                'B' || B_PC.model || B_pc.code name,
                B_pc.price,
                B_pc.TYPE,
                B_pc.cpu,
                'none' AS feature
            FROM
                PC B_pc,
                (
                SELECT 
                    AVG(B_computer.price) average_price,
                    AVG(B_computer.cpu) average_cpu
                FROM
                    (
                    SELECT
                        price price,
                        cpu cpu
                    FROM
                        PC 		
                    ) B_computer
                    ) B_computer_averages
            WHERE 
                B_PC .price < B_computer_averages.average_price
                AND B_PC .cpu > B_computer_averages.average_cpu

        """):
            table.append(list(row))

    for each in table:
        print("{: >6} {: >6} {: >6} {: >6} {: >6}".format(*each))


def fetch_televisions_closest_price(connection: cx_Oracle.connect) -> None:
    # get user input
    price = input('Enter price: ')
    if not price.strip().isdigit():
        print('Error: Invalid input.')
        print('Error: Please enter proper integer.')
        sys.exit()

    print("\n-------------------------------------\n")
    table = [
        ['NAME', 'PRICE', 'TYPE', 'SCREEN SIZE'],
        ['----', '-----', '----', '----------'],
    ]
    # fetch closest priced televisions
    with connection.cursor() as cursor:
        for row in cursor.execute("""
            SELECT 
                televisions.name, 
                televisions.price, 
                televisions.TYPE,
                televisions.screen_size
            FROM
                (
                SELECT
                    'A' || A_HDTV.model name,
                    A_HDTV.price,
                    'H' AS TYPE,
                    A_HDTV.screen_size
                FROM
                    HDTV A_hdtv
            UNION
                SELECT
                    'A' || A_PDPTV.model name,
                    A_PDPTV .PRICE,
                    'P' AS TYPE,
                    A_PDPTV .SCREEN_SIZE
                FROM
                    PDPTV A_pdptv
            UNION
                SELECT
                    'A' || A_LCDTV.model name,
                    A_LCDTV .PRICE ,
                    'L' AS TYPE,
                    A_LCDTV .SCREEN_SIZE
                FROM
                    LCDTV A_lcdtv
            UNION
                SELECT
                    'B' || B_TV.model || B_TV .CODE name,
                    B_TV .PRICE,
                    B_TV ."TYPE" ,
                    B_TV .SCREEN_SIZE
                FROM
                    TV B_tv
                ) televisions,
                (
                SELECT
                    price
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                        ) Television
                    ORDER BY
                        ABS( television.price - :price ) ASC
                    )
                WHERE
                    ROWNUM <2
                ) closest_price
            WHERE
                televisions.price = closest_price.price
        """, price=int(price)
        ):
            table.append(list(row))

    for each in table:
        print("{: >6} {: >6} {: >6} {: >6}".format(*each))


def fetch_televisions_recommended(connection: cx_Oracle.connect) -> None:
    print("\n-------------------------------------\n")
    table = [
        ['NAME', 'PRICE', 'TYPE', 'SCREEN SIZE'],
        ['----', '-----', '----', '----------'],
    ]
    # fetch recommended televisions
    with connection.cursor() as cursor:
        for row in cursor.execute("""
            SELECT 
                name, 
                price, 
                TYPE, 
                screen_size
            FROM
                (
                SELECT
                    name,
                    price,
                    TYPE,
                    screen_size,
                    (screen_size / price) ratio
                FROM
                    (
                    SELECT
                        'A' || A_HDTV.model name,
                        A_HDTV.price,
                        'H' AS TYPE,
                        A_HDTV.screen_size
                    FROM
                        HDTV A_hdtv,
                        (
                        SELECT
                            AVG(A_tv.price) average_price,
                            AVG(A_tv.screen_size) average_size
                        FROM
                            (
                            SELECT
                                A_HDTV.price,
                                A_HDTV.screen_size
                            FROM
                                HDTV A_hdtv
                        UNION
                            SELECT
                                A_PDPTV.PRICE,
                                A_PDPTV.SCREEN_SIZE
                            FROM
                                PDPTV A_pdptv
                        UNION
                            SELECT
                                A_LCDTV.PRICE ,
                                A_LCDTV.SCREEN_SIZE
                            FROM
                                LCDTV A_lcdtv
                    ) A_tv
                ) A_tv_averages
                    WHERE
                        price < A_tv_averages.average_price
                        AND SCREEN_SIZE > A_tv_averages.average_size
                UNION
                    SELECT
                        'A' || A_PDPTV.model name,
                        A_PDPTV .PRICE,
                        'P' AS TYPE,
                        A_PDPTV .SCREEN_SIZE
                    FROM
                        PDPTV A_pdptv,
                        (
                        SELECT
                            AVG(A_tv.price) average_price,
                            AVG(A_tv.screen_size) average_size
                        FROM
                            (
                            SELECT
                                A_HDTV.price,
                                A_HDTV.screen_size
                            FROM
                                HDTV A_hdtv
                        UNION
                            SELECT
                                A_PDPTV.PRICE,
                                A_PDPTV.SCREEN_SIZE
                            FROM
                                PDPTV A_pdptv
                        UNION
                            SELECT
                                A_LCDTV.PRICE ,
                                A_LCDTV.SCREEN_SIZE
                            FROM
                                LCDTV A_lcdtv
                    ) A_tv
                ) A_tv_averages
                    WHERE
                        price < A_tv_averages.average_price
                        AND SCREEN_SIZE > A_tv_averages.average_size
                UNION
                    SELECT
                        'A' || A_LCDTV.model name,
                        A_LCDTV .PRICE ,
                        'L' AS TYPE,
                        A_LCDTV .SCREEN_SIZE
                    FROM
                        LCDTV A_lcdtv,
                        (
                        SELECT
                            AVG(A_tv.price) average_price,
                            AVG(A_tv.screen_size) average_size
                        FROM
                            (
                            SELECT
                                A_HDTV.price,
                                A_HDTV.screen_size
                            FROM
                                HDTV A_hdtv
                        UNION
                            SELECT
                                A_PDPTV.PRICE,
                                A_PDPTV.SCREEN_SIZE
                            FROM
                                PDPTV A_pdptv
                        UNION
                            SELECT
                                A_LCDTV.PRICE ,
                                A_LCDTV.SCREEN_SIZE
                            FROM
                                LCDTV A_lcdtv
                    ) A_tv
                ) A_tv_averages
                    WHERE
                        price < A_tv_averages.average_price
                        AND SCREEN_SIZE > A_tv_averages.average_size
                UNION
                    SELECT
                        'B' || B_TV.model || B_TV .CODE name,
                        B_TV .PRICE,
                        B_TV ."TYPE" ,
                        B_TV .SCREEN_SIZE
                    FROM
                        TV B_tv,
                        (
                        SELECT
                            AVG(B.price) average_price,
                            AVG(B.screen_size) average_size
                        FROM
                            (
                            SELECT
                                price,
                                screen_size
                            FROM
                                TV
                
                    ) B
                ) B_tv_averages
                    WHERE
                        price < B_tv_averages.average_price
                        AND SCREEN_SIZE > B_tv_averages.average_size
                )
                ORDER BY
                    ratio DESC 
                )
            WHERE rownum < 2
        """):
            table.append(list(row))

    for each in table:
        print("{: >6} {: >6} {: >6} {: >6}".format(*each))


def update_computers(connection: cx_Oracle.connect) -> None:
    A_desktop_keys = []
    A_laptop_keys = []
    B_pc_keys = []
    with connection.cursor() as cursor:
        # fetch models in DESKTOP to be updated.
        for row in cursor.execute("""
            SELECT
                *
            FROM
                DESKTOP A_desktop,
                (
                SELECT
                    AVG(PC_ALL.price) average_price,
                    AVG(PC_ALL.cpu) average_cpu
                FROM
                    (
                    SELECT
                        A_desktop.model name,
                        A_DESKTOP.price price,
                        'D' AS TYPE,
                        A_DESKTOP.cpu cpu,
                        'none' AS feature
                    FROM
                        DESKTOP A_desktop
                    UNION

                    SELECT
                        A_LAPTOP.model name,
                        A_LAPTOP.PRICE,
                        'L' AS TYPE,
                        A_LAPTOP.CPU,
                        TO_CHAR(A_LAPTOP.WEIGHT) AS feature
                    FROM
                        LAPTOP A_LAPTOP
                    UNION

                    SELECT
                        B_PC.model,
                        B_pc.price,
                        B_pc.TYPE,
                        B_pc.cpu,
                        'none' AS feature
                    FROM
                        PC B_pc
                    ) PC_ALL
                ) PC_averages
            WHERE
                A_desktop.cpu < pc_averages.average_cpu
        """):
            A_desktop_keys.append(row[0])

        # fetch models in LAPTOP to be updated.
        for row in cursor.execute("""
            SELECT
                *
            FROM
                LAPTOP A_LAPTOP,
                (
                SELECT
                    AVG(PC_ALL.price) average_price,
                    AVG(PC_ALL.cpu) average_cpu
                FROM
                    (
                    SELECT
                        A_desktop.model name,
                        A_DESKTOP.price price,
                        'D' AS TYPE,
                        A_DESKTOP.cpu cpu,
                        'none' AS feature
                    FROM
                        DESKTOP A_desktop
                    UNION

                    SELECT
                        A_LAPTOP.model name,
                        A_LAPTOP.PRICE,
                        'L' AS TYPE,
                        A_LAPTOP.CPU,
                        TO_CHAR(A_LAPTOP.WEIGHT) AS feature
                    FROM
                        LAPTOP A_LAPTOP
                    UNION

                    SELECT
                        B_PC.model,
                        B_pc.price,
                        B_pc.TYPE,
                        B_pc.cpu,
                        'none' AS feature
                    FROM
                        PC B_pc
                    ) PC_ALL
                ) PC_averages
            WHERE
                A_LAPTOP.cpu < pc_averages.average_cpu
        """):
            A_laptop_keys.append(row[0])

        # fetch models and code in PC to be updated
        for row in cursor.execute("""
            SELECT
                *
            FROM
                PC B_PC,
                (
                SELECT
                    AVG(PC_ALL.price) average_price,
                    AVG(PC_ALL.cpu) average_cpu
                FROM
                    (
                    SELECT
                        A_desktop.model name,
                        A_DESKTOP.price price,
                        'D' AS TYPE,
                        A_DESKTOP.cpu cpu,
                        'none' AS feature
                    FROM
                        DESKTOP A_desktop
                    UNION

                    SELECT
                        A_LAPTOP.model name,
                        A_LAPTOP.PRICE,
                        'L' AS TYPE,
                        A_LAPTOP.CPU,
                        TO_CHAR(A_LAPTOP.WEIGHT) AS feature
                    FROM
                        LAPTOP A_LAPTOP
                    UNION

                    SELECT
                        B_PC.model,
                        B_pc.price,
                        B_pc.TYPE,
                        B_pc.cpu,
                        'none' AS feature
                    FROM
                        PC B_pc
                    ) PC_ALL
                ) PC_averages
            WHERE
                B_PC.cpu < pc_averages.average_cpu
        """):
            B_pc_keys.append((row[0], row[1]))

    # update prices
    with connection.cursor() as cursor:
        cursor.executemany("""
            UPDATE
                DESKTOP
            SET
                price = (0.9) * price
            WHERE
                model = :1
        """, [(model,) for model in A_desktop_keys])

        cursor.executemany("""
            UPDATE
                LAPTOP
            SET
                price = (0.9) * price
            WHERE
                model = :1
        """, [(model,) for model in A_laptop_keys])

        cursor.executemany("""
            UPDATE
                PC
            SET
                price = (0.9) * price
            WHERE
                model = :1
                AND code = :2
        """, [(model, code) for model, code in B_pc_keys])

        connection.commit()

    A_desktop_to_delete = []
    A_laptop_to_delete = []
    B_pc_to_delete = []

    with connection.cursor() as cursor:
        # fetch most expensive models in DESKTOP if exists
        for row in cursor.execute("""
            SELECT
                *
            FROM
                DESKTOP A_desktop,
                (
                SELECT
                    price
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            A_desktop.model name,
                            A_DESKTOP.price price,
                            'D' AS TYPE,
                            A_DESKTOP.cpu cpu,
                            'none' AS feature
                        FROM
                            DESKTOP A_desktop
                    UNION
                        SELECT
                            A_LAPTOP.model name,
                            A_LAPTOP.PRICE,
                            'L' AS TYPE,
                            A_LAPTOP.CPU,
                            TO_CHAR(A_LAPTOP.WEIGHT) AS feature
                        FROM
                            LAPTOP A_LAPTOP
                    UNION
                        SELECT
                            B_PC.model,
                            B_pc.price,
                            B_pc.TYPE,
                            B_pc.cpu,
                            'none' AS feature
                        FROM
                            PC B_pc
                        ) PC_ALL
                    ORDER BY
                        PC_ALL.price DESC
                )
                WHERE
                    rownum < 2
                ) Most_expensive
            WHERE
                A_desktop.price = Most_expensive.price
        """):
            A_desktop_to_delete.append(row[0])

        # fetch most expensive models in LAPTOP if exists
        for row in cursor.execute("""
            SELECT
                *
            FROM
                LAPTOP A_LAPTOP,
                (
                SELECT
                    price
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            A_desktop.model name,
                            A_DESKTOP.price price,
                            'D' AS TYPE,
                            A_DESKTOP.cpu cpu,
                            'none' AS feature
                        FROM
                            DESKTOP A_desktop
                    UNION
                        SELECT
                            A_LAPTOP.model name,
                            A_LAPTOP.PRICE,
                            'L' AS TYPE,
                            A_LAPTOP.CPU,
                            TO_CHAR(A_LAPTOP.WEIGHT) AS feature
                        FROM
                            LAPTOP A_LAPTOP
                    UNION
                        SELECT
                            B_PC.model,
                            B_pc.price,
                            B_pc.TYPE,
                            B_pc.cpu,
                            'none' AS feature
                        FROM
                            PC B_pc
                        ) PC_ALL
                    ORDER BY
                        PC_ALL.price DESC
                )
                WHERE
                    rownum < 2
                ) Most_expensive
            WHERE
                A_LAPTOP.price = Most_expensive.price
        """):
            A_laptop_to_delete.append(row[0])

        # fetch most expensive models and code in PC if exists
        for row in cursor.execute("""
            SELECT
                *
            FROM
                PC B_PC,
                (
                SELECT
                    price
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            A_desktop.model name,
                            A_DESKTOP.price price,
                            'D' AS TYPE,
                            A_DESKTOP.cpu cpu,
                            'none' AS feature
                        FROM
                            DESKTOP A_desktop
                    UNION
                        SELECT
                            A_LAPTOP.model name,
                            A_LAPTOP.PRICE,
                            'L' AS TYPE,
                            A_LAPTOP.CPU,
                            TO_CHAR(A_LAPTOP.WEIGHT) AS feature
                        FROM
                            LAPTOP A_LAPTOP
                    UNION
                        SELECT
                            B_PC.model,
                            B_pc.price,
                            B_pc.TYPE,
                            B_pc.cpu,
                            'none' AS feature
                        FROM
                            PC B_pc
                        ) PC_ALL
                    ORDER BY
                        PC_ALL.price DESC
                )
                WHERE
                    rownum < 2
                ) Most_expensive
            WHERE
                B_PC.price = Most_expensive.price
        """):
            B_pc_keys.append((row[0], row[1]))

    # delete most expensive items
    with connection.cursor() as cursor:
        cursor.executemany("""
            DELETE
            FROM
                DESKTOP
            WHERE
                model = :1
        """, [(model,) for model in A_desktop_to_delete])

        cursor.executemany("""
            DELETE
            FROM
                LAPTOP
            WHERE
                model = :1
        """, [(model,) for model in A_laptop_to_delete])

        cursor.executemany("""
            DELETE
            FROM
                PC
            WHERE
                model = :1
                AND code = :2
        """, [(model, code) for model, code in B_pc_to_delete])

        connection.commit()

    print('Computer prices are updated...')


def update_televisions(connection: cx_Oracle.connect) -> None:
    A_hdtv_keys = []
    A_pdptv_keys = []
    A_lcdtv_keys = []
    B_tv_keys = []
    with connection.cursor() as cursor:
        # fetch models in HDTV to be updated.
        for row in cursor.execute("""
            SELECT
                *
            FROM
                HDTV A_hdtv,
                (
                SELECT
                    biggest_size.screen_size max_size
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                    ) TV_all
                        ORDER BY
                            TV_all.screen_size DESC
                ) biggest_size
                WHERE
                    rownum < 2
                )max_size
            WHERE
                max_size.max_size = A_hdtv.screen_size
        """):
            A_hdtv_keys.append(row[0])

        # fetch models in PDPTV to be updated.
        for row in cursor.execute("""
            SELECT
                *
            FROM
                PDPTV A_pdptv,
                (
                SELECT
                    biggest_size.screen_size max_size
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                ) TV_all
                    ORDER BY
                        TV_all.screen_size DESC
            ) biggest_size
                WHERE
                    rownum < 2
                )max_size
            WHERE
                max_size.max_size = A_PDPTV.screen_size
        """):
            A_pdptv_keys.append(row[0])

        # fetch models in LCDTV to be updated.
        for row in cursor.execute("""
            SELECT
                *
            FROM
                LCDTV A_lcdtv,
                (
                SELECT
                    biggest_size.screen_size max_size
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                ) TV_all
                    ORDER BY
                        TV_all.screen_size DESC
            ) biggest_size
                WHERE
                    rownum < 2
                )max_size
            WHERE
                max_size.max_size = A_LCDTV.screen_size
        """):
            A_lcdtv_keys.append(row[0])

        # fetch models in TV to be updated.
        for row in cursor.execute("""
            SELECT
                *
            FROM
                TV B_TV,
                (
                SELECT
                    biggest_size.screen_size max_size
                FROM
                    (
                    SELECT
                        *
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                ) TV_all
                    ORDER BY
                        TV_all.screen_size DESC
            ) biggest_size
                WHERE
                    rownum < 2
                )max_size
            WHERE
                max_size.max_size = B_TV.screen_size
        """):
            B_tv_keys.append((row[0], row[1]))

    # update prices
    with connection.cursor() as cursor:
        cursor.executemany("""
            UPDATE
                HDTV
            SET
                price = (1.1) * price
            WHERE
                model = :1
        """, [(model,) for model in A_hdtv_keys])

        cursor.executemany("""
            UPDATE
                PDPTV
            SET
                price = (1.1) * price
            WHERE
                model = :1
        """, [(model,) for model in A_pdptv_keys])

        cursor.executemany("""
            UPDATE
                LCDTV
            SET
                price = (1.1) * price
            WHERE
                model = :1
        """, [(model,) for model in A_lcdtv_keys])

        cursor.executemany("""
            UPDATE
                TV
            SET
                price = (1.1) * price
            WHERE
                model = :1
                AND code = :2
        """, [(model, code) for model, code in B_tv_keys])

        connection.commit()

    A_hdtv_to_delete = []
    A_pdptv_to_delete = []
    A_lcdtv_to_delete = []
    B_tv_to_delete = []

    with connection.cursor() as cursor:
        # fetch biggest ratio models in HDTV if exists
        for row in cursor.execute("""
            SELECT
                A_HDTV.MODEL,
                (A_HDTV.screen_size / A_HDTV.price) AS ratio
            FROM
                HDTV A_hdtv,
                (
                SELECT
                    TV_ratio.ratio max_ratio
                FROM
                    (
                    SELECT
                        (TV_all.screen_size / TV_all.price) AS ratio
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                    ) TV_all
                    ORDER BY
                        ratio DESC
                    ) TV_ratio
                WHERE
                    rownum < 2
                    
                ) Biggest_ratio
            WHERE
                (A_HDTV.screen_size / A_HDTV.price) = Biggest_ratio.max_ratio
        """):
            A_hdtv_to_delete.append(row[0])

        # fetch biggest ratio models in PDPTV if exists
        for row in cursor.execute("""
            SELECT
                A_PDPTV.MODEL,
                (A_PDPTV.screen_size / A_PDPTV.price) AS ratio
            FROM
                PDPTV A_PDPTV,
                (
                SELECT
                    TV_ratio.ratio max_ratio
                FROM
                    (
                    SELECT
                        (TV_all.screen_size / TV_all.price) AS ratio
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                    ) TV_all
                    ORDER BY
                        ratio DESC
                    ) TV_ratio
                WHERE
                    rownum < 2
                    
                ) Biggest_ratio
            WHERE
                (A_PDPTV.screen_size / A_PDPTV.price) = Biggest_ratio.max_ratio
        """):
            A_pdptv_to_delete.append(row[0])

        # fetch biggest ratio models in LCDTV if exists
        for row in cursor.execute("""
            SELECT
                A_LCDTV.MODEL,
                (A_LCDTV.screen_size / A_LCDTV.price) AS ratio
            FROM
                LCDTV A_LCDTV,
                (
                SELECT
                    TV_ratio.ratio max_ratio
                FROM
                    (
                    SELECT
                        (TV_all.screen_size / TV_all.price) AS ratio
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                    ) TV_all
                    ORDER BY
                        ratio DESC
                    ) TV_ratio
                WHERE
                    rownum < 2
                    
                ) Biggest_ratio
            WHERE
                (A_LCDTV.screen_size / A_LCDTV.price) = Biggest_ratio.max_ratio
        """):
            A_lcdtv_to_delete.append(row[0])

        # fetch biggest ratio models in TV if exists
        for row in cursor.execute("""
            SELECT
                B_TV.MODEL,
                B_TV.CODE,
                (B_TV.screen_size / B_TV.price) AS ratio
            FROM
                TV B_TV,
                (
                SELECT
                    TV_ratio.ratio max_ratio
                FROM
                    (
                    SELECT
                        (TV_all.screen_size / TV_all.price) AS ratio
                    FROM
                        (
                        SELECT
                            'A' || A_HDTV.model name,
                            A_HDTV.price,
                            'H' AS TYPE,
                            A_HDTV.screen_size
                        FROM
                            HDTV A_hdtv
                    UNION
                        SELECT
                            'A' || A_PDPTV.model name,
                            A_PDPTV .PRICE,
                            'P' AS TYPE,
                            A_PDPTV .SCREEN_SIZE
                        FROM
                            PDPTV A_pdptv
                    UNION
                        SELECT
                            'A' || A_LCDTV.model name,
                            A_LCDTV .PRICE ,
                            'L' AS TYPE,
                            A_LCDTV .SCREEN_SIZE
                        FROM
                            LCDTV A_lcdtv
                    UNION
                        SELECT
                            'B' || B_TV.model || B_TV .CODE name,
                            B_TV .PRICE,
                            B_TV ."TYPE" ,
                            B_TV .SCREEN_SIZE
                        FROM
                            TV B_tv
                    ) TV_all
                    ORDER BY
                        ratio DESC
                    ) TV_ratio
                WHERE
                    rownum < 2
                    
                ) Biggest_ratio
            WHERE
                (B_TV.screen_size / B_TV.price) = Biggest_ratio.max_ratio
        """):
            B_tv_to_delete.append((row[0], row[1]))

    # delete biggest ratio items
    with connection.cursor() as cursor:
        cursor.executemany("""
            DELETE
            FROM
                HDTV
            WHERE
                model = :1
        """, [(model,) for model in A_hdtv_to_delete])
        cursor.executemany("""
            DELETE
            FROM
                PDPTV
            WHERE
                model = :1
        """, [(model,) for model in A_pdptv_to_delete])

        cursor.executemany("""
            DELETE
            FROM
                LCDTV
            WHERE
                model = :1
        """, [(model,) for model in A_lcdtv_to_delete])

        cursor.executemany("""
            DELETE
            FROM
                TV
            WHERE
                model = :1
                AND code = :2
        """, [(model, code) for model, code in B_tv_to_delete])

        connection.commit()

    print('Television prices are updated...')


class UIHandler:

    def __init__(self, connection: cx_Oracle.connect) -> None:
        self.connection = connection
        self.response_welcome_page(self.show_welcome_page())

    def _get_menu_selection_user_input(self, max_menu_index: int) -> int:
        user_input = input('Enter number: ')
        if not user_input.strip().isdigit():
            print('Error: Invalid input.')
            print('Error: Please enter proper integer.')
            sys.exit()
        if max_menu_index < int(user_input) or int(user_input) <= 0:
            print('Error: Invalid input.')
            print('Error: Out of range.')
            sys.exit()
        return int(user_input)

    def print_exit_message(self) -> None:
        print("--- GOOD BYE! ---")
        sys.exit()

    def show_welcome_page(self) -> int:
        print("\n-------------------------------------\n")
        print("Welcome to the \'bagaji.com\'!")
        print("\n-------------------------------------\n")
        print("What are you looking for?")
        print("1. Computer")
        print("2. Television")
        print("3. Price update")
        print("4. Exit")
        return self._get_menu_selection_user_input(4)

    def response_welcome_page(self, selection: int) -> None:
        if selection == 1:
            self.response_computer_page(self.show_computer_page())
        if selection == 2:
            self.response_television_page(self.show_television_page())
        if selection == 3:
            self.response_price_update()
        if selection == 4:
            self.print_exit_message()

    def show_computer_page(self) -> int:
        print("\n-------------------------------------\n")
        print("- Computer -")
        print("1. Product list")
        print("2. Recommended products")
        print("3. Back")
        return self._get_menu_selection_user_input(3)

    def response_computer_page(self, selection: int) -> None:
        if selection == 1:
            fetch_computers_order_by_name(self.connection)
        if selection == 2:
            fetch_computers_recommended(self.connection)
        if selection == 3:
            self.response_welcome_page(self.show_welcome_page())
        self.response_computer_page(self.show_computer_page())

    def show_television_page(self) -> int:
        print("\n-------------------------------------\n")
        print("- Television -")
        print("1. Search by price")
        print("2. Recommended products")
        print("3. Back")
        return self._get_menu_selection_user_input(3)

    def response_television_page(self, selection: int) -> None:
        if selection == 1:
            fetch_televisions_closest_price(self.connection)
        if selection == 2:
            fetch_televisions_recommended(self.connection)
        if selection == 3:
            self.response_welcome_page(self.show_welcome_page())
        self.response_television_page(self.show_television_page())

    def response_price_update(self) -> None:
        print("\n-------------------------------------\n")
        update_computers(self.connection)
        update_televisions(self.connection)
        print("Update success.")
        self.response_welcome_page(self.show_welcome_page())


if __name__ == "__main__":
    connection = make_connection()
    if connection is False:
        print_connection_error()
        sys.exit()

    menu = UIHandler(connection)
